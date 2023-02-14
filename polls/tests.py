
import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse

class QuestionModelTests(TestCase):

    def test_was_published_recently_future_questions(self):
        """Was_published_recently return False for questions whose pub_date is in the future"""
        time=timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text = "¿Quien es el mejor Course Directo de Platzi", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_past_questions(self):
        """Was_published_recently return False for questions whose pub_date is in the past"""
        time=timezone.now() - datetime.timedelta(days=30)
        past_question = Question(question_text = "¿Quien es el mejor Course Directo de Platzi", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_present_questions(self):
        """Was_published_recently return True for questions whose pub_date is in the present"""
        time=timezone.now()
        present_question = Question(question_text = "¿Quien es el mejor Course Directo de Platzi", pub_date=time)
        self.assertIs(present_question.was_published_now(), True)

def create_question(question_text, days):
    """Create a question with the given 'question_text' and published the given number
    of 'days' offset to now (negative for questions published in the past, positive
    for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTest(TestCase):

    def test_no_question(self):
        """If no question exist, an appropiated mesagge is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_no_future_question_are_displayed(self):
        """If a future question is created in the database, this question is not show until its pub_date is equal to the present time"""
        response = self.client.get(reverse("polls:index"))
        time = timezone.now() + datetime.timedelta(days = 30)
        future_question = Question (question_text = "¿Quien es el mejor estudiante de Platzi", pub_date = time)
        self.assertNotIn(future_question, response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        #print("test_past_question")
        time = timezone.now() + datetime.timedelta(days=-5)
        past_question = Question.objects.create(question_text="question_text", pub_date=time)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_future_question_and_past_question(self):
        #print("test_future_question_and_past_question")
        """"Even if both past and future question exist, only past question are display"""
        past_question = create_question(question_text = "Past question", days = -30)
        future_question = create_question(question_text="Future question", days = 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_two_future_question(self):
        """The question index page may display multiple questions"""
        future_question1 = create_question(question_text = "Future question 1", days = 0)
        future_question2 = create_question(question_text="Future question 2", days = 0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [future_question1, future_question2]
        )
        
    def test_two_past_question(self):
        """The question index page may display multiple questions"""
        past_question1 = create_question(question_text = "Past question 1", days = -30)
        past_question2 = create_question(question_text="Future question 2", days = -40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )

class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        The detail view a question with a pub_date in the future
        returns a 404 error not found
        """
        future_question = create_question(question_text="Future Question 3", days = 35)
        url = reverse("polls:get_queryset", args =(future_question.id,))
        response = self.client.get(url)
        print('***********************************************************')
        print(response)

        self.assertEqual(response.status_code, 404)


    def test_past_question(self):
        """
        The detail view a question with a pub_date in the past
        displays the question's text
        """
        past_question = create_question(question_text="Past Question 3", days = -30)
        url = reverse("polls:get_queryset", args =(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
