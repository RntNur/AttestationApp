from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from app.models import Tours, Category


class TourAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(pk = 2)  # надо учесть - создан экземпляр Category с id=2, либо другой
        self.tour = Tours.objects.create(name = 'Test Tour',
                                         description = 'Test Description',
                                         price = 200.0,
                                         exist = True,
                                         category = self.category)  # тестовый объекта тур

    def test_tour_update(self):
        url = reverse('tour_api_detail', args = [self.tour.pk])
        data = {
            'name': 'UpdatedTestTour',
            'description': 'Updated Test Description',
            'price': 200.0,
            'exist': True,
            'category': self.category.pk,  # Здесь надо учесть id категории, либо создать новую
        }
        response = self.client.put(url, data, format = 'json')
        print(response.data)
        self.assertEqual(response.data['message'], 'Данные успешно изменены')


    def test_tour_detail(self):
        url = reverse('tour_api_detail', args = [self.tour.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tour_delete(self):
        url = reverse('tour_api_detail', args = [self.tour.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tours.objects.filter(pk = self.tour.pk).exists())
