from django.test import TestCase
from django.core.urlresolvers import reverse

from rango.models import Category

# Create your tests here.

class CategoryMethodTests(TestCase):
	
	def test_ensure_views_are_positive(self):
		cat = Category(name='test', views = -1, likes = 0)
		cat.save()
		self.assertEqual((cat.views >= 0), True)

	def test_slug_line_creation(self):
		cat = Category(name = 'Random Category String!')
		cat.save()
		self.assertEqual(cat.slug, 'random-category-string')



class IndexViewTests(TestCase):
	
	def test_index_view_with_no_categories(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no categories present.")
		self.assertQuerysetEqual(response.context['categories'], [])

	# add a helpler method
	def add_cat(name, views, likes):
		c = Category.objects.get_or_create(name = name)[0]
		c.views = views
		c.likes = likes
		c.save()
		return c
	# add a test method to test presenting categories.
	def test_index_view_with_categories(self):
		add_cat('test', 1, 1)
		add_cat('tet', 1, 1)
		add_cat('tt', 1, 1)
		add_cat('tst', 1, 1)
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "tst")

		num_cats = len(response.context['categories'])
		self.assertEqual(num_cats, 4)

