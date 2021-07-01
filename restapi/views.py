# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.http import HttpResponse
#
# # Create your views here.
#
#
# def index():
#     return HttpResponse("Hello, world. You're at Rest.")
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from restapi.quiz_main.quiz_service import QuizService
from rest_framework import serializers



@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def quiz_create(request):
    """
    Creates a quiz data
    """
    
    error_code = 400
    try:
        params = request.data
        if 'name' not in params:
            raise Exception("Internal error: name is missing")
        if 'description' not in params:
            raise Exception("Internal error: description is missing")

        qs = QuizService(params)
        quiz_data = qs.create_quiz()
        return Response(quiz_data, status=201)
    except Exception as e:
        resp_data = {"status": "failure", "reason": str(e)}
        results = ErrorResponseSerializer(resp_data).data
        return Response(results, status=error_code)


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def quiz_get(request, quiz_id):
    """
    gets the quiz data
    """
    error_code = 400
    try:
        if not quiz_id:
            raise Exception("Internal error: quiz id is missing")
        quiz_id = quiz_id.replace(':', '')
        qd = QuizService({"quiz_id":int(quiz_id)})
        quiz_details = qd.get_quiz()
        if not quiz_details:
            return Response(quiz_details, status=404)
        return Response(quiz_details, status=200)
    except Exception as e:
        resp_data = {"status": "failure", "reason": str(e)}
        results = ErrorResponseSerializer(resp_data).data
        return Response(results, status=error_code)


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def question_get(request, question_id):
    """
    gets the question data
    """
    error_code = 400
    try:
        if not question_id:
            raise Exception("Internal error: quiz id is missing")
        question_id = question_id.replace(":", "")
        qs = QuizService({"question_id":int(question_id)})
        quiz_details = qs.get_question()
        if not quiz_details:
            return Response(quiz_details, status=404)
        return Response(quiz_details, status=200)
    except Exception as e:
        resp_data = {"status": "failure", "reason": str(e)}
        results = ErrorResponseSerializer(resp_data).data
        return Response(results, status=error_code)


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def question_create(request):
    """
    creates teh question
    """
    error_code = 400
    try:
        params = request.data
        if 'name' not in params:
            raise Exception("Internal error: name is missing")
        if 'options' not in params:
            raise Exception("Internal error: options are missing")
        if 'correct_option' not in params:
            raise Exception("Internal error: correct option is missing")
        if 'quiz' not in params:
            raise Exception("Internal error: quiz id is missing")
        if 'points' not in params:
            raise Exception("Internal error: points are  missing")

        qs = QuizService(params)
        question_data = qs.create_question()
        return Response(question_data, status=201)
    except Exception as e:
        resp_data = {"status": "failure", "reason": str(e)}
        results = ErrorResponseSerializer(resp_data).data
        return Response(results, status=error_code)

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def quiz_questions_get(request, quiz_id):
    """
    gets the quiz and question detail
    """
    error_code = 400
    try:
        if not quiz_id:
            raise Exception("Internal error: quiz id is missing")
        quiz_id = quiz_id.replace(":", "")
        qd = QuizService({"quiz_id":int(quiz_id)})
        quiz_details = qd.quiz_questions()
        if not quiz_details:
            return Response(quiz_details, status=404)
        return Response(quiz_details, status=200)
    except Exception as e:
        resp_data = {"status": "failure", "reason": str(e)}
        results = ErrorResponseSerializer(resp_data).data
        return Response(results, status=error_code)


class ErrorResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    reason = serializers.CharField()
