#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
from pytodoist import todoist
import ToDoist as todo
import TrainingMenus as menu

def Training2Todoist(event,context):
     limit = todo.ConvTime(22,15)

     # Choice Training Menus
     tmenus = random.sample(range(4),int(os.environ['NUMBER_OF_TRAININGS']))

     # LogIn to ToDoist
     user = todo.login()

     project = user.get_project("Inbox")
     #    project = user.get_project("🏥健康管理")
     task = project.add_task("トレーニング",date=limit)
     
     for row in range(int(os.environ['NUMBER_OF_TRAININGS'])):
          t = tmenus[row]
          # Choice Training Program Version
          v = random.randrange(1,3,1)
          title = menu.menu[t][0]
          url   = menu.menu[t][v]

          task.add_note(str(title) + "\n" + str(url))
          task.update()

     return limit