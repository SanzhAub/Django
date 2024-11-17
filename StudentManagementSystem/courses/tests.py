from django.test import TestCase
from courses.models import Course
from django.core.cache import cache
from users.models import User

class CourseModelTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(username="instructor", password="password123")
        
    def test_create_course(self):
        course = Course.objects.create(
            name="Mathematics",
            description="Basic Math Course",
            instructor=self.instructor
        )
        self.assertIsNotNone(course.id)
class CourseCacheTest(TestCase):
    def test_course_cache(self):
        course = Course.objects.create(name='Physics', description='Physics course')
        cache.set('course_list', [course], 60)

        cached_courses = cache.get('course_list')
        self.assertEqual(len(cached_courses), 1)
        self.assertEqual(cached_courses[0].name, 'Physics')
