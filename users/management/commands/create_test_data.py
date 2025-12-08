from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from designs.models import Design
from comments.models import Comment
from social.models import Like, Bookmark, Follow
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test data for FabSketch'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')
        
        # Create test users
        users = self.create_users()
        self.stdout.write(f'Created {len(users)} users')
        
        # Create test designs
        designs = self.create_designs(users)
        self.stdout.write(f'Created {len(designs)} designs')
        
        # Create test comments
        comments = self.create_comments(users, designs)
        self.stdout.write(f'Created {len(comments)} comments')
        
        # Create social interactions
        self.create_social_interactions(users, designs)
        self.stdout.write('Created social interactions')
        
        self.stdout.write(self.style.SUCCESS('Test data created successfully!'))

    def create_users(self):
        users_data = [
            {'username': 'designer1', 'nickname': '패션디자이너김', 'bio': '트렌디한 디자인을 추구합니다'},
            {'username': 'designer2', 'nickname': '스타일리스트박', 'bio': '미니멀한 스타일 전문가'},
            {'username': 'designer3', 'nickname': '크리에이터이', 'bio': '독창적인 아이디어로 승부'},
            {'username': 'designer4', 'nickname': '아티스트최', 'bio': '예술적 감각의 패션 디자인'},
            {'username': 'viewer1', 'nickname': '패션러버', 'bio': '패션을 사랑하는 일반인'},
        ]
        
        users = []
        for data in users_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'nickname': data['nickname'],
                    'bio': data['bio'],
                    'profile_image': f'https://picsum.photos/200/200?random={random.randint(1, 100)}'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
            users.append(user)
        
        return users

    def create_designs(self, users):
        designs_data = [
            {
                'title': '봄 캐주얼 블라우스',
                'description': '가벼운 소재로 제작된 봄철 캐주얼 블라우스입니다. 데일리룩으로 완벽해요!',
                'hashtags': ['봄패션', '캐주얼', '블라우스', '데일리룩'],
                'materials': '면 70%, 폴리에스터 30%'
            },
            {
                'title': '미니멀 원피스',
                'description': '심플하면서도 세련된 디자인의 원피스. 어떤 상황에도 어울려요.',
                'hashtags': ['미니멀', '원피스', '세련됨', '심플'],
                'materials': '린넨 100%'
            },
            {
                'title': '빈티지 데님 재킷',
                'description': '레트로 감성이 물씬 나는 데님 재킷. 개성 있는 스타일링이 가능합니다.',
                'hashtags': ['빈티지', '데님', '재킷', '레트로'],
                'materials': '코튼 데님 100%'
            },
            {
                'title': '여름 시원한 티셔츠',
                'description': '통풍이 잘 되는 소재로 만든 여름용 티셔츠. 시원하고 편안해요.',
                'hashtags': ['여름', '티셔츠', '시원함', '편안함'],
                'materials': '모달 60%, 코튼 40%'
            },
            {
                'title': '우아한 이브닝 드레스',
                'description': '특별한 날을 위한 우아한 이브닝 드레스. 고급스러운 실루엣이 매력적입니다.',
                'hashtags': ['이브닝', '드레스', '우아함', '특별한날'],
                'materials': '실크 80%, 폴리에스터 20%'
            },
        ]
        
        designs = []
        for i, data in enumerate(designs_data):
            design, created = Design.objects.get_or_create(
                title=data['title'],
                defaults={
                    'user': users[i % len(users[:4])],  # Only designers create designs
                    'description': data['description'],
                    'hashtags': data['hashtags'],
                    'materials': data['materials'],
                    'sketch_url': f'https://picsum.photos/400/600?random={i+10}',
                    'flat_url': f'https://picsum.photos/400/600?random={i+20}',
                    'wearing_url': f'https://picsum.photos/400/600?random={i+30}',
                    'view_count': random.randint(10, 500)
                }
            )
            designs.append(design)
        
        return designs

    def create_comments(self, users, designs):
        comments_data = [
            '정말 예쁜 디자인이네요! 어디서 구매할 수 있나요?',
            '색감이 너무 좋아요. 다른 색상도 있나요?',
            '이런 스타일 정말 좋아해요. 팔로우 할게요!',
            '소재가 궁금해요. 착용감은 어떤가요?',
            '와 진짜 예술작품 같아요 👏',
            '이 디자인 영감을 어디서 받으셨나요?',
            '실제로 보면 더 예쁠 것 같아요',
            '다음 작품도 기대됩니다!',
        ]
        
        comments = []
        for design in designs:
            # Each design gets 2-5 random comments
            num_comments = random.randint(2, 5)
            for _ in range(num_comments):
                comment = Comment.objects.create(
                    design=design,
                    user=random.choice(users),
                    content=random.choice(comments_data)
                )
                comments.append(comment)
        
        return comments

    def create_social_interactions(self, users, designs):
        # Create likes (each design gets 3-15 likes)
        for design in designs:
            num_likes = random.randint(3, 15)
            liked_users = random.sample(users, min(num_likes, len(users)))
            for user in liked_users:
                Like.objects.get_or_create(design=design, user=user)
        
        # Create bookmarks (each design gets 1-8 bookmarks)
        for design in designs:
            num_bookmarks = random.randint(1, 8)
            bookmarked_users = random.sample(users, min(num_bookmarks, len(users)))
            for user in bookmarked_users:
                Bookmark.objects.get_or_create(design=design, user=user)
        
        # Create follows (users follow each other randomly)
        for user in users:
            # Each user follows 1-3 other users
            num_follows = random.randint(1, 3)
            other_users = [u for u in users if u != user]
            followed_users = random.sample(other_users, min(num_follows, len(other_users)))
            for followed_user in followed_users:
                Follow.objects.get_or_create(follower=user, followee=followed_user)
