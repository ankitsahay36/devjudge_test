from restapi.db_service.mongodb.mongo_service import MongoDBClient
import json


class QuizService:
    import os
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'config.json')
    with open(file_path, 'r') as f:
        __collection_details = json.load(f)['collections']
        pass
    __quiz_data = "quiz_details"
    __question_data = "question_details"
    __typ_l = [__quiz_data, __question_data]

    def __init__(self, params={}):
        self.params = params
        self.mongo_client = MongoDBClient()

    def create_quiz(self):
        try:
            qfilter = {}
            quiz_data = self.mongo_client.get(self.__collection_details[self.__quiz_data], qfilter)
            post_n = len(quiz_data)+1
            pre_n = 10**5
            final_quiz_id = pre_n + post_n
            new_dic = dict()
            new_dic['id'] = final_quiz_id
            new_dic.update(self.params)
            self.insert_data(new_dic, 0, id=final_quiz_id)
            return new_dic
        except Exception as e:
            raise Exception("Quiz creation failed" + str(e))

    def create_question(self):
        try:
            qfilter = {}
            quizfilter = {"id":self.params["quiz"]}
            quiz_data = self.mongo_client.get(self.__collection_details[self.__quiz_data], quizfilter)
            if not quiz_data:
                raise Exception("There is no quiz with the given quiz id")
            question_data = self.mongo_client.get(self.__collection_details[self.__question_data], qfilter)
            post_n = len(question_data)+1
            pre_n = 10**7
            final_quiz_id = pre_n + post_n
            new_dic = dict()
            new_dic['id'] = final_quiz_id
            new_dic.update(self.params)
            self.insert_data(new_dic, 1, id=final_quiz_id)
            return new_dic
        except Exception as e:
            raise Exception("Question creation failed - " + str(e))

    def insert_data(self, data, type, **kwargs):
        try:
            self.mongo_client.save(self.__collection_details[self.__typ_l[type]], data, **kwargs)
        except Exception as e:
            raise Exception("Data creation failed" + str(e))

    def get_quiz(self):
        try:
            qfilter = {"id":self.params["quiz_id"]}
            quiz_data = self.mongo_client.get(self.__collection_details[self.__quiz_data], qfilter)
            if not quiz_data:
                return {}
            return quiz_data[0]
        except Exception as e:
            raise Exception("Quiz fetch failed - " + str(e))

    def get_question(self):
        try:
            qfilter = {"id":self.params["question_id"]}
            question_data = self.mongo_client.get(self.__collection_details[self.__question_data], qfilter)
            if not question_data:
                return {}
            return question_data[0]
        except Exception as e:
            raise Exception("Question fetch failed - " + str(e))

    def quiz_questions(self):
        try:
            qfilter = {"id":self.params["quiz_id"]}
            question_filter = {"quiz": self.params["quiz_id"]}
            question_data = self.mongo_client.get(self.__collection_details[self.__question_data], question_filter)
            quiz_data = self.mongo_client.get(self.__collection_details[self.__quiz_data], qfilter)
            if not quiz_data:
                raise Exception("There is no quiz with the given quiz id")
            quiz_data = quiz_data[0]
            quiz_data.pop("id")
            quiz_data["questions"] = question_data
            return quiz_data
        except Exception as e:
            raise Exception("Question fetch failed - " + str(e))


if __name__ == "__main__":
    ob = QuizService({
    "name": "second question first quiz",
    "options": "data",
    "correct_option":"3" ,
    "quiz": 100001,
    "points": 4
})
    print(ob.create_question())


