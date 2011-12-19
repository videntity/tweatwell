
README.rst for the Django Quiz Application
==========================================

This application is designed to facilitate online multiple-choce quizes with
required questions, random questions, and question that, if asked, the user
must get right.  The quiz application displays the final score, and wheather
the score is passing or failing.  The pass/fail threshold (MIN_QUIZ_PASS_SCORE)
is set in models.py Its defaulted to 75%.  Note that even if the user has a
passing score, he or she will still fail if a "must get right" Question is
missed. The number of random questions (QUIZ_NUM_RAND_QUESTIONS) is also set in
models.py.  The application will attempt to add this number of questions within
the category (ie. where alwaysask=False & category=[current_quiz_category]).
If not enough questions are available in the category, the application will just
ask as many as it can.  Grading/scorring will still work correctly in this case.

Admin users also have access to a dashboard that provides
a summary for each quiz in aggregate and broken down by category.

Define question categories (same as quiz types), questions, and their respective
answers using the (Django) admin interface.  Its best to create these items in
the afformentioned order.  Note that when defining answers, you are defining
all multiple choice answers and tagging one Answer per question as the correct
answer.

You should never need to create quizes or Responses in the admin.  These are
generated/updated automatically as the user takes and completes the quiz.


Key URLS:
=========

The key urls are as follows....


http://../quiz/category/[catname]
"""Take the quize of type category, where [catname] is a valid category."""

http://../quiz/complete/[catname]
"""The completed score sheet, , where [catname] is a valid category."""

http://../quiz/dashboard
"""The admin/staff summary page.  You must be staff or superuser to see
this page."""



Good Luck!

-Alan Viars