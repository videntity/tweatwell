from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from datetime import date, datetime
from quiz.models import Category, Question, Answer, Quiz, Response 
from quiz.urls import *
from quiz.models import Quiz, QUIZ_NUM_RAND_QUESTIONS, MIN_QUIZ_PASS_SCORE 

"""
Tests for the Quiz app. It assumes 4 questions are asked in the quiz.
2 required question and 2 random questions. The test user is Testy McTesterson.
The username and password are testy/pass. Make sure you dont leave first and
last name blank. 'video' is a valid category in the test fixtures.

Run with "manage.py test".  Example:
Example: python manage.py test auth quiz --settings=gr.settings.dev

Generate the test data
python manage.py dumpdata quiz --settings=gr.settings.dev > ./apps/quiz/fixtures/testdata.json
"""
QUIZ_NUM_REQUIRED_QUESTIONS_FOR_TEST = 2
QUIZ_TOTAL_NUM_QUESTIONS_FOR_TEST = QUIZ_NUM_REQUIRED_QUESTIONS_FOR_TEST + QUIZ_NUM_RAND_QUESTIONS
USERNAME_FOR_TEST='testy'
PASSWORD_FOR_TEST='pass'
VALID_QUIZ_ID_FOR_TEST=34
INVALID_QUIZ_ID_FOR_TEST=999
VALID_QUIZ_CATEGORY='video'
INVALID_QUIZ_CATEGORY='foo'
STAFF_USERNAME_FOR_TEST='alan'
STAFF_PASSWORD_FOR_TEST='pass'

class SimpleTest(TestCase):
    """A bootstrap to check the testing environment is working"""
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

class CreateQuizTypeVideoWhereUserAlreadyPassed_TestCase(TestCase):
    """
    Create a quiz where user already passed should not display quiz but
    instead a message saying the user has already passed.
    """
    fixtures=['already_passed_data.json']

    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict={}
        self.url=reverse('take_quiz', kwargs={'category': VALID_QUIZ_CATEGORY})
        
    def test_get_take_quiz_where_category_is_video_and_user_already_passed_should_respond_200(self):
        """GET take_quiz (category=video) (quiz.passed=True) should return HTTP response 200 (OK)"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 200)

        
    def test_get_take_quiz_where_category_is_video_and_user_already_passed_should_contain_text(self):
        """GET take_quiz (category=video) (quiz.passed=True) should contain text"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertContains(response, "You already passed")
        
class CreateQuizTypeVideoWhereNoQuizForUser_TestCase(TestCase):
    """Create a new quiz for a first timer."""
    fixtures=['no_quizes_testdata.json']

    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('take_quiz', kwargs={'category': VALID_QUIZ_CATEGORY})
        
    def test_get_take_quiz_where_category_is_video_and_user_already_passed_should_respond_200(self):
        """GET take_quiz (category=video) (quiz=None) should return HTTP response 200 (OK)"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 200)
        
    def test_get_take_quiz_where_category_is_video_and_user_already_passed_should_contain_text(self):
        """GET take_quiz (category=video) (quiz=None) should contain text (OK)"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertContains(response, "Answer the questions below to Join the Rocket Community:")
        
        
class CreateQuizTypeVideoWhereUserPreviousFailedQuiz_TestCase(TestCase):
    """Create a quiz where user has failed in the past."""
    fixtures=['one_past_failed_quiz_testdata.json']

    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('take_quiz', kwargs={'category': VALID_QUIZ_CATEGORY})
        
    def test_get_take_quiz_where_category_is_video_and_user_has_taken_quiz_but_not_yet_passed_should_respond_200(self):
        """GET take_quiz (category=video) (quiz.passed=False) should return HTTP response 200 (OK)"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 200)
        
        
    def test_get_take_quiz_where_category_is_video_and_user_has_taken_quiz_but_not_yet_passed_should_contain_text(self):
        """GET take_quiz (category=video) (quiz.passed=False) should contain text"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertContains(response, "Answer the questions below to Join the Rocket Community:") 


class CreateQuizWithNonExistentCategoryType_TestCase(TestCase):
    """ Create a quize with a non-existent Category type"""
    fixtures=['one_past_failed_quiz_testdata.json']

    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('take_quiz', kwargs={'category': INVALID_QUIZ_CATEGORY})
        
    def test_get_take_quiz_where_category_does_not_exist_should_respond_404(self):
        """GET take_quiz (category=foo) should return HTTP response 404 (PageNotFound)"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 404)
        
        
class ViewCompletedQuizScoreSheetWhereUserFailedQuiz_TestCase(TestCase):
    """View a completed score care where user fails the quiz"""
    fixtures=['one_past_failed_quiz_testdata.json']

    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('quiz_complete', kwargs={'category': VALID_QUIZ_CATEGORY})
        
    def test_get_display_completed_where_user_failed_latest_should_respond_200(self):
        """GET completed should return HTTP response 200 (OK)"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 200)
    
        
    def test_get_display_completed_where_user_failed_latest_should_contain_text(self):
        """GET completed should contain text"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertContains(response, "Test Complete")
        self.assertContains(response, "Unfortunately you didn't pass")
        self.assertContains(response, "Your score was:")
        self.assertContains(response, "Here are the answers and explanations for the ones you missed.")

class ViewCompletedQuizScoreSheetWhereUserPassedQuizButMissedSome_TestCase(TestCase):
    """View a passing but not perfect score card."""
    fixtures=['one_passed_quiz_testdata.json']

    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('quiz_complete', kwargs={'category': VALID_QUIZ_CATEGORY})
        
    def test_get_display_completed_where_user_passed_but_missed_some_should_respond_200(self):
        """GET completed should return HTTP response 200 (OK)"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 200)
        self.url=reverse('quiz_complete', kwargs={'category': VALID_QUIZ_CATEGORY})

    def test_get_display_completed_where_user_passed_but_missed_some_should_contain_text(self):
        """GET completed should contain text"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertContains(response, "Test Complete")
        self.assertContains(response, "You've passed! Congratulations")
        self.assertContains(response, "Your score was:")
        self.assertContains(response, "Here are the answers and explanations for the ones you missed.")


class ViewCompletedQuizScoreSheetWhereUserPassedQuizWithPerfectScore_TestCase(TestCase):
    """View a perfect score scorecard"""
    fixtures=['one_perfect_score_quiz_testdata.json']

    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('quiz_complete', kwargs={'category': VALID_QUIZ_CATEGORY})
        
    def test_get_display_completed_where_user_passed_but_missed_some_should_respond_200(self):
        """GET completed should return HTTP response 200 (OK)"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 200)
        
        
    def test_get_display_completed_where_user_passed_but_missed_some_should_contain_text(self):
        """GET completed should contain certain text"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertContains(response, "Your score was:")
        self.assertContains(response, "100")
        self.assertContains(response, "You didn't miss a single question")
        
        
class ViewCompletedQuizScoreSheetWhereFailsBecauseHeMissedAMustGetRightQuestion_TestCase(TestCase):
    """Check to make sure a user fails quiz if he misses a question where must_get_right=True"""
    fixtures=['missed_a_must_get_right_question_testdata.json']

    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('quiz_complete', kwargs={'category': VALID_QUIZ_CATEGORY})
        
    def test_get_display_completed_where_user_failed_because_missed_mustgetright_should_respond_200(self):
        """GET completed should return HTTP response 200 (OK)"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 200)
        
        
    def test_get_display_completed_where_user_failed_because_missed_mustgetright_should_contain_text(self):
        """GET completed should contain certain text"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertContains(response, "Test Complete")
        self.assertContains(response, "Unfortunately you didn't pass")
        self.assertContains(response, "Your score was:")
        self.assertContains(response, "Here are the answers and explanations for the ones you missed.")
        
class ViewCompletedQuizWhereMethodPOST_TestCase(TestCase):
    """View a completed score care where user fails the quiz"""
    fixtures=['one_past_failed_quiz_testdata.json']

    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('quiz_complete', kwargs={'category': VALID_QUIZ_CATEGORY})
        
    def test_post_display_completed_should_respond_405(self):
        """POST completed should return HTTP response 405 (Method Not Allowed)"""
        response = self.client.post(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 405)
    
    


 
        
class ViewCompletedQuizScoreSheetValidateScoring_TestCase(TestCase):
    """ Validate that the scoring/grading works."""
    fixtures=['passed_quiz_with_75_percent_testdata.json']

    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('quiz_complete', kwargs={'category': VALID_QUIZ_CATEGORY})
        self.number_right=3
        
    def test_get_display_completed_score_should_validate(self):
        """GET completed should contain the score of the user"""
        
        response = self.client.get(self.url, self.dict)
        grade = (float(self.number_right) / float(QUIZ_TOTAL_NUM_QUESTIONS_FOR_TEST)) * 100
        grade=int(grade)
        # Check some response details
        self.assertContains(response, grade)

class ViewCompletedQuizScoreSheetValidateFailOnLowScore_TestCase(TestCase):
    """ Validate that the scoring/grading works."""
    fixtures=['failed_quiz_with_50_percent_testdata.json']

    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('quiz_complete', kwargs={'category': VALID_QUIZ_CATEGORY})
        self.number_right=2
        
    def test_get_display_completed_fails_if_score_below_min_passscore(self):
        """The user should fail if his score is less than the minimum"""
        
        response = self.client.get(self.url, self.dict)
        
        grade = (float(self.number_right) / float(QUIZ_TOTAL_NUM_QUESTIONS_FOR_TEST)) * 100
        grade=int(grade)
        # Check some response details
        self.assertTrue(grade<MIN_QUIZ_PASS_SCORE)
        self.assertContains(response, "Unfortunately you didn't pass")


class ProcessIncompleteQuiz_TestCase(TestCase):
    """Test processing of an incomplete quiz"""
    
    fixtures=['quiz_without_answers_testdata.json']
    
    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {'quizid': VALID_QUIZ_ID_FOR_TEST,
                     'closest-sun':'mercury',
                     'color-tree-leaves':'green', }
        self.url=reverse('take_quiz', kwargs={'category':VALID_QUIZ_CATEGORY})
    
    def test_post_process_incomplete_quiz_should_respond_200(self):
        """POST incomplete quiz should return HTTP response 200 (OK)"""
        response = self.client.post(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 200)
        
    def test_post_process_incomplete_quiz_should_contain_text(self):
        """POST incomplete quiz should contain text "You didn't answer all the questions" """
        response = self.client.post(self.url, self.dict)
        # Check some response details
        self.assertContains(response, "You didn't answer all the questions")
        

class ProcessValidQuiz_TestCase(TestCase):
    """Test processing of a valid quiz"""
    fixtures=['quiz_without_answers_testdata.json']
    
    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {'quizid': VALID_QUIZ_ID_FOR_TEST,
                     'closest-sun':'mercury',
                     'color-tree-leaves':'green',
                     'use-workproduct-promotion':'Yes',
                     'what-format-best-deliver-logo-client':'AI Adobe Illustrator',
                     }
        self.url=reverse('take_quiz', kwargs={'category':VALID_QUIZ_CATEGORY})
    
    def test_post_process_complete_quiz_should_respond_302(self):
        """POST complete quiz should return HTTP respond with 302 (Redirect)"""
        response = self.client.post(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 302)


    def test_post_process_complete_quiz_should_redirect_to_complete(self):
        """POST complete quiz should redirect to complete"""
        response = self.client.post(self.url, self.dict)
        # Check some response details
        self.assertRedirects(response, reverse('quiz_complete', kwargs={'category': VALID_QUIZ_CATEGORY}) )
        

class ProcessQuizWithInvalidQuizID_TestCase(TestCase):
    """Process a quiz with an unvalid Quizid"""
    fixtures=['quiz_without_answers_testdata.json']
    
    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {'quizid': INVALID_QUIZ_ID_FOR_TEST,
                     'closest-sun':'mercury',
                     'color-tree-leaves':'green',
                     'use-workproduct-promotion':'Yes'}
        self.url=reverse('take_quiz', kwargs={'category':VALID_QUIZ_CATEGORY})
    
    def test_post_process_complete_quiz_with_invalid_quizid_should_respond_404(self):
        """POST complete quiz with invalid QuizID should return HTTP response 404 (NOT FOUND)"""
        response = self.client.post(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 404)
        


class ViewQuizAdminDashboardWithMethodPost_TestCase(TestCase):
    """Display the admin dashboard with a HTTP method POST"""
    fixtures=['quiz_without_answers_testdata.json']
    
    def setUp(self):
        self.client=Client()
        self.client.login(username=STAFF_USERNAME_FOR_TEST,
                          password=STAFF_PASSWORD_FOR_TEST)
        self.dict = {'quizid': INVALID_QUIZ_ID_FOR_TEST,
                     'closest-sun':'mercury',
                     'color-tree-leaves':'green',
                     'use-workproduct-promotion':'Yes'}
        self.url=reverse('dashboard')
    
    def test_post_view_quiz_admin_dashboard_respond_405(self):
        """POST display quiz admin dashboard should return HTTP response 405 (METHOD NOT ALLOWED)"""
        response = self.client.post(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 405)



class ViewQuizAdminDashboardWithoutWhereIsStaffFalse_TestCase(TestCase):
    """Non-staff tries to view quiz admin dashboard"""
    fixtures=['testy_user_isStaffFalse_testdata.json']
    
    def setUp(self):
        self.client=Client()
        self.client.login(username=USERNAME_FOR_TEST, password=PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('dashboard')
    
    def test_get_view_quiz_admin_dashboard_with_isStaff_False_should_respond_403(self):
        """
        GET quiz admin dashboard where user.is_staff=False should
        return HTTP response 403 (Forbidden)
        """
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 403)




class ViewQuizAdminDashboardWithNoData_TestCase(TestCase):
    """View Quiz admin dashboard with no database"""
    fixtures=['no_quizes_testdata.json']
    
    def setUp(self):
        self.client=Client()
        self.client.login(username=STAFF_USERNAME_FOR_TEST, password=STAFF_PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('dashboard')
    
    def test_get_view_quiz_admin_dashboard_with_no_data_should_respond_200(self):
        """GET dashboard where no quiz data exists should return HTTP response 200 (OK)"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 200)
        
class ViewQuizAdminDashboardCorrectlyCalclulatedPassFailRatio_TestCase(TestCase):
    """Make sure the dashboard Correcly calcuates Total Pass/Fali Ratio"""
    fixtures=['test_passfail_ratio_calculate_testdata.json']
    

    def setUp(self):
        self.client=Client()
        self.client.login(username=STAFF_USERNAME_FOR_TEST, password=STAFF_PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('dashboard')
        self.number_quiz_takers=Quiz.objects.filter(score__gt=-1).aggregate(num_users=Count('user', distinct=True))
        self.number_quiz_takers=self.number_quiz_takers['num_users']
        self.num_tries = len(Quiz.objects.filter(score__gt=-1))    


        
    def test_get_display_admin_correct_ratio(self):
        """Calculate the pass/fail ratio."""
        
        response = self.client.get(self.url, self.dict)
        
        ratio=float(self.num_tries)/float(self.number_quiz_takers)
        ratio=round(ratio,2)

        # Check some response details
        self.assertContains(response, ratio)

    def test_get_view_quiz_admin_calculate_ratio_should_respond_200(self):
        """GET dashboard when calculating ratio should return HTTP response 200 (OK)"""
        response = self.client.get(self.url, self.dict)
        # Check some response details
        self.assertEqual(response.status_code, 200)
        
        
        
class ViewQuizAdminDashboardWherePassFailRatioUnavailable_TestCase(TestCase):
    """If not enough data exists the ratio should not be displayed but still respond 200"""
    fixtures=['no_quizes_testdata.json']
    

    def setUp(self):
        self.client=Client()
        self.client.login(username=STAFF_USERNAME_FOR_TEST, password=STAFF_PASSWORD_FOR_TEST)
        self.dict = {}
        self.url=reverse('dashboard')
       

        
    def test_get_display_admin_no_ratio_should_contain_unavailable(self):
        """Calculate the pass/fail ratio."""
        
        response = self.client.get(self.url, self.dict)

        # Check some response details
        self.assertContains(response, "Unavailable")