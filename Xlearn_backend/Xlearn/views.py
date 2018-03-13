from .models import*
from django.contrib.auth.models import User
from django.contrib import auth
from codex.baseview import APIView
from codex.baseerror import LogicError, LoginRequired, AuthorityError, VerifyError
from django.core.mail import send_mail
import datetime
import random
import string
import os
from django.db.models import ObjectDoesNotExist
import json


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIGS = json.loads(open(os.path.join(BASE_DIR, 'configs.json')).read())


class TaskDetail(APIView):
    def get(self):
        self.check_input('id')
        get_id = self.input['id']
        try:
            task = Task.objects.get(id = get_id)
        except ObjectDoesNotExist:
            raise LogicError("No Task!")

        return {
            'config': json.load(task.config),
            'creator': task.creator.username,
            'name' : task.name,
            'description': task.description,
            'create_at': task.created_at,
            'status': task.status,
            'input_model': task.input_model,
            'type': task.type,
            'link': task.dataset.link,
            'path': task.dataset.path,
            'dataset_status': task.dataset.status,

        }


    def post(self):
        self.check_input("task_config")
        my_task = self.input["task_config"]
        own_dataset = Dataset.objects.create(
            link = my_task["link"],
            status = my_task["status"],
            path = "/static/" + my_task["link"],
        )
        optimizer = Optimizer.objects.create(
            name = my_task["optimizer_name"],
            parameters = my_task["optimizer_parameters"],
            type = my_task["optimizer_type"]
        )

        network = Network.objects.create(
            name=my_task["network_name"],
            parameters=my_task["network_parameters"],
            type = my_task["network_type"]

        )
        loss = Loss.objects.create(
            name=my_task["loss_name"],
            parameters=my_task["loss_parameters"],
            type = my_task["loss_type"],

        )
        config_task = {
            "optimizer_name":my_task["optimizer_name"],
            'optimizer_parameters': my_task["optimizer_parameters"],
            "network_name": my_task["network_name"],
            'network_parameters': my_task["network_parameters"],
            "loss_name": my_task["loss_name"],
            'loss_parameters': my_task["loss_parameters"],
        }

        new_task = Task.objects.create(
            name = my_task["name"],
            description = my_task["description"],
            status = my_task["status"],
            created_at = my_task["created_at"],
            input_model = my_task["input_model"],
            type = my_task["type"],
            dataset = own_dataset,
            config = json.dumps(config_task)


        )
        own_dataset.task = new_task
        own_dataset.save()


class TaskList(APIView):
    def get(self):
        result = []
        task_list = Task.objects.all()
        for task in task_list:
            result.append(
                {
                    'config': json.load(task.config),
                    'creator': task.creator.username,
                    'name': task.name,
                    'description': task.description,
                    'instance': task.instance.id,
                    'create_at': task.created_at,
                    'status': task.status,
                    'input_model': task.input_model,
                    'type': task.type,
                    'link': task.dataset.link,
                    'path': task.dataset.path,
                    'dataset_status': task.dataset.status,
                }
            )
        return result


class NetworkList(APIView):
    def get(self):
        self.check_input("type")
        data = []
        network_list = Network.objects.filter(type = self.input["type"])
        for network in network_list:
            data.append(
                {
                    'name': network.name,
                    'type': network.type,
                    'parameters': json.load(network.parameters),
                }
            )

        return data


class OptimizerList(APIView):
    def get(self):
        self.check_input("type")
        data = []
        optimizer_list = Optimizer.objects.filter(type=self.input["type"])
        for optimizer in optimizer_list:
            data.append(
                {
                    'name': optimizer.name,
                    'type': optimizer.type,
                    'parameters': json.load(optimizer.parameters),
                }
            )

        return data


class LossList(APIView):
    def get(self):
        self.check_input("type")
        data = []
        loss_list = Network.objects.filter(type=self.input["type"])
        for loss in loss_list:
            data.append(
                {
                    'name': loss.name,
                    'type': loss.type,
                    'parameters': json.load(loss.parameters),
                }
            )

        return data


class InstanceDetail(APIView):
    def get(self):
        self.check_input('id')
        get_id = self.input['id']
        try:
            instance = Instance.objects.get(id = get_id)
        except ObjectDoesNotExist:
            raise LogicError("No Instance!")

        return {
            'config': json.load(instance.config),
            'creator': instance.creator.username,
            'name' : instance.name,
            'description': instance.description,
            'create_at': instance.created_at,
            'status': instance.status,
            'input_model': instance.input_model,
            'type': instance.type,
            'link': instance.dataset.link,
            'path': instance.dataset.path,
            'dataset_status': instance.dataset.status,
            'run_time': instance.run_time,

        }

















