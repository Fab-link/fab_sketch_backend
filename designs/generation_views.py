import json
import boto3
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import base64
from PIL import Image
from io import BytesIO

# AWS clients
lambda_client = boto3.client('lambda', region_name='ap-northeast-2')
s3_client = boto3.client('s3', region_name='ap-northeast-2')

S3_BUCKET_NAME = 'fab-sketch-media-xp8zu198'
LAMBDA_FUNCTION_NAME = 'fabsketch-gen'

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_design(request):
    """
    Generate 3 design images from sketch
    Expected payload:
    {
        "image": "base64_string",
        "category": "adult_clothing",
        "gender": "unisex", 
        "type": "top",
        "style": "casual"
    }
    """
    try:
        # Validate input
        image_data = request.data.get('image')
        category = request.data.get('category')
        gender = request.data.get('gender')
        clothing_type = request.data.get('type')
        style = request.data.get('style', 'casual')
        
        if not all([image_data, category, gender, clothing_type]):
            return Response({
                'error': 'Missing required fields: image, category, gender, type'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Prepare lambda payload
        lambda_payload = {
            'action': 'generate_full_collection',
            'session_id': session_id,
            'image_data': image_data,
            'parameters': {
                'category': category,
                'gender': gender,
                'type': clothing_type,
                'style': style
            }
        }
        
        # Call lambda function
        response = lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,
            InvocationType='RequestResponse',
            Payload=json.dumps(lambda_payload)
        )
        
        # Parse lambda response
        lambda_result = json.loads(response['Payload'].read())
        
        if response['StatusCode'] != 200:
            return Response({
                'error': 'Lambda function failed',
                'details': lambda_result
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Return result with S3 URLs
        return Response({
            'session_id': session_id,
            'status': 'completed',
            'step_1': lambda_result.get('step_1'),  # Final Design
            'step_2': lambda_result.get('step_2'),  # Tech Flat  
            'step_3': lambda_result.get('step_3'),  # Try-On
            'specs_log': lambda_result.get('specs_log')
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Design generation failed',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_design_to_feed(request):
    """
    Save generated design to feed
    Expected payload:
    {
        "session_id": "uuid",
        "title": "Design Title",
        "description": "Design Description", 
        "hashtags": "#fashion #design",
        "materials": "Cotton 100%",
        "selected_images": ["final_design", "try_on"]
    }
    """
    try:
        from .models import Design
        
        session_id = request.data.get('session_id')
        title = request.data.get('title')
        description = request.data.get('description')
        hashtags = request.data.get('hashtags', '')
        materials = request.data.get('materials', '')
        selected_images = request.data.get('selected_images', ['final_design'])
        
        if not all([session_id, title, description]):
            return Response({
                'error': 'Missing required fields: session_id, title, description'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get image URLs from S3 based on session_id
        sketch_url = f"https://{S3_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{session_id}/sketch.jpg"
        final_design_url = f"https://{S3_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{session_id}/step_1.jpg"
        tech_flat_url = f"https://{S3_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{session_id}/step_2.jpg"
        try_on_url = f"https://{S3_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{session_id}/step_3.jpg"
        
        # Determine main image for feed based on selection
        if 'final_design' in selected_images:
            main_image_url = final_design_url
        elif 'try_on' in selected_images:
            main_image_url = try_on_url
        else:
            main_image_url = final_design_url
        
        # Create design record
        design = Design.objects.create(
            user=request.user,
            title=title,
            description=description,
            image_url=main_image_url,
            sketch_url=sketch_url,
            tech_flat_url=tech_flat_url,
            try_on_url=try_on_url,
            hashtags=hashtags,
            materials=materials,
            session_id=session_id
        )
        
        return Response({
            'message': 'Design saved to feed successfully',
            'design_id': design.id,
            'design': {
                'id': design.id,
                'title': design.title,
                'description': design.description,
                'image_url': design.image_url,
                'sketch_url': design.sketch_url,
                'tech_flat_url': design.tech_flat_url,
                'try_on_url': design.try_on_url,
                'hashtags': design.hashtags,
                'materials': design.materials,
                'created_at': design.created_at
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': 'Failed to save design',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_generation_status(request, session_id):
    """
    Check generation status for a session
    """
    try:
        # Check if files exist in S3
        files_to_check = ['step_1.jpg', 'step_2.jpg', 'step_3.jpg']
        completed_files = []
        
        for file_name in files_to_check:
            try:
                s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=f"{session_id}/{file_name}")
                completed_files.append(file_name)
            except:
                pass
        
        if len(completed_files) == 3:
            status_result = 'completed'
        elif len(completed_files) > 0:
            status_result = 'in_progress'
        else:
            status_result = 'pending'
        
        return Response({
            'session_id': session_id,
            'status': status_result,
            'completed_files': completed_files,
            'progress': len(completed_files) / 3 * 100
        })
        
    except Exception as e:
        return Response({
            'error': 'Failed to check status',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
