# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.path = [[0,0]]
        self.current_pos = [0,0]  #first index is column, second index is row
        self.home = True
        self.once_left = False
        self.direction = 1  # 1 for right, 2 for up, 3 for left, 4 for down
        self.pos_achieved = [[0,0]]  #history
        self.temp_dir = 0  # used to change direction if want to turn round
        self.gold_found = False  #flag (will be True if found "G")
        self.safe_pos = []  #a list contains safe position or potential safe position
        self.unsafe_pos = []  #didn't use now (want to save unsafe position)
        self.world_size = [-1,-1]  #-1 means don't know yet
        self.should_go_home = False
        self.isgoing = False
        self.is_scream = False
        self.has_shoot = False
        self.once_safe = True
        self.spos = []
        self.bpos = []

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        
        if (self.is_safe(stench,breeze)):
            self.update_safe_pos()
        self.check_safe_pos()
        
        if glitter:
            self.gold_found = True
            return Agent.Action.GRAB;

        if scream:
            self.is_scream = True
            
##        if (stench and self.home == True):
##            if self.has_shoot == False:
##                self.has_shoot = True
##                return Agent.Action.SHOOT
        
        if self.gold_found or self.no_safe_pos():  #
##            print("current_pos: " + str(self.current_pos) )
##            print("direction: " + str(self.direction) )
##            print("path: " + str(self.path) )
            return self.go_home()

        elif (breeze and self.home == True):
            return Agent.Action.CLIMB

        elif (stench and self.home == True):
            if self.is_scream == False:
                if self.has_shoot == False:
                    self.has_shoot = True
                    return Agent.Action.SHOOT
                else:
                    self.home = False
                    self.once_left = True
                    return self.go_to([1,0])
                    


        elif bump:
            self.reset_pos()
            self.change_direction(Agent.Action.TURN_LEFT)
            return Agent.Action.TURN_LEFT


            
        if (self.once_left == False):
            self.once_left = True
            self.home = False
            
        if (self.is_safe(stench,breeze)):
            if len(self.pos_achieved) > 1:
                if (self.once_left == True and self.current_pos == [0,0]):
                    self.home = True
                    return  Agent.Action.CLIMB
                
            if self.current_pos not in self.safe_pos:
                self.safe_pos.append(self.current_pos[:])
            self.update_safe_pos()  #save current pos to safe

            self.set_go_back_dir() #used to turn round

            adjacent_pos = [[self.current_pos[0]+1, self.current_pos[1]],
                            [self.current_pos[0]-1, self.current_pos[1]],
                            [self.current_pos[0], self.current_pos[1]+1],
                            [self.current_pos[0], self.current_pos[1]-1]]  #get adjacent pos before update current pos
            goal_pos = self.update_pos()  #move forward
##            print("current: " + str(self.current_pos))
##            print("dir: " + str(self.direction))
##            print("goal: " + str(goal_pos))
##            print("achieved_pos: " + str(self.pos_achieved))
##            print("safe_pos: " + str(self.safe_pos))
##            print("path: " + str(self.path))
            
            if goal_pos in self.safe_pos:
                if (goal_pos not in self.pos_achieved):
                    return self.go_to(goal_pos)
            for pos in adjacent_pos:
                if (pos in self.safe_pos and (pos not in self.pos_achieved)):
                    return self.go_to(pos)
                
            if len(self.path) <= 1:
                return self.go_to(self.path[0])
            if (self.isgoing == False):
                self.path.pop()  #now go back 1 step
            return self.go_to(self.path[-1])

        elif(stench and (not breeze)):
            self.spos.append(self.current_pos)
##            if (([self.current_pos[0]+1, self.current_pos[1]+1] in self.bpos) and ([self.current_pos[0]+1, self.current_pos[1]+1] not in self.spos)):
##                if ([self.current_pos[0], self.current_pos[1]+1] not in self.pos_achieved):
##                    print("1")
##                    return self.go_to([self.current_pos[0], self.current_pos[1]+1])
##                if ([self.current_pos[0]+1, self.current_pos[1]] not in self.pos_achieved):
##                    print("2")
##                    return self.go_to([self.current_pos[0]+1, self.current_pos[1]])
##            if (([self.current_pos[0]+1, self.current_pos[1]-1] in self.bpos) and ([self.current_pos[0]+1, self.current_pos[1]-1] not in self.spos)):
##                if ([self.current_pos[0], self.current_pos[1]-1] not in self.pos_achieved):
##                    return self.go_to([self.current_pos[0], self.current_pos[1]-1])
##                if ([self.current_pos[0]+1, self.current_pos[1]] not in self.pos_achieved):
##                    return self.go_to([self.current_pos[0]+1, self.current_pos[1]])
##            if (([self.current_pos[0]-1, self.current_pos[1]-1] in self.bpos) and ([self.current_pos[0]-1, self.current_pos[1]-1] not in self.spos)):
##                if ([self.current_pos[0], self.current_pos[1]-1] not in self.pos_achieved);
##                    return self.go_to([self.current_pos[0], self.current_pos[1]-1])
##                if ([self.current_pos[0]-1, self.current_pos[1]] not in self.pos_achieved);
##                    return self.go_to([self.current_pos[0]-1, self.current_pos[1]]) 
                
            if (self.is_scream == True):
                if len(self.pos_achieved) > 1:
                    if (self.once_left == True and self.current_pos == [0,0]):
                        self.home = True
                        return  Agent.Action.CLIMB
                    
                if self.current_pos not in self.safe_pos:
                    self.safe_pos.append(self.current_pos[:])
                self.update_safe_pos()  #save current pos to safe

                self.set_go_back_dir() #used to turn round

                adjacent_pos = [[self.current_pos[0]+1, self.current_pos[1]],
                                [self.current_pos[0]-1, self.current_pos[1]],
                                [self.current_pos[0], self.current_pos[1]+1],
                                [self.current_pos[0], self.current_pos[1]-1]]  #get adjacent pos before update current pos
                goal_pos = self.update_pos()  #move forward
##                print("current: " + str(self.current_pos))
##                print("dir: " + str(self.direction))
##                print("goal: " + str(goal_pos))
##                print("achieved_pos: " + str(self.pos_achieved))
##                print("safe_pos: " + str(self.safe_pos))
##                print("path: " + str(self.path))
                
                if goal_pos in self.safe_pos:
                    if (goal_pos not in self.pos_achieved):
                        return self.go_to(goal_pos)
                for pos in adjacent_pos:
                    if (pos in self.safe_pos and (pos not in self.pos_achieved)):
                        return self.go_to(pos)
                    
                if len(self.path) <= 1:
                    return self.go_to(self.path[0])
                if (self.isgoing == False):
                    self.path.pop()  #now go back 1 step
                return self.go_to(self.path[-1])
            else:
                if len(self.pos_achieved) > 1:
                    if (self.once_left == True and self.current_pos == [0,0]):
                        self.home = True
                        return  Agent.Action.CLIMB
                if self.has_shoot == False:
                    self.has_shoot = True
                    return Agent.Action.SHOOT
                if self.once_safe == True:
                    self.once_safe = False
                    goal_pos = self.update_pos()
##                    self.update_safe_pos()
##                    print("nob")
                    return self.go_to(goal_pos)
                if self.current_pos == [0,0]:
                    return Agent.Action.CLIMB
                goal_pos = self.update_pos()
                adjacent_pos = [[self.current_pos[0]+1, self.current_pos[1]],
                            [self.current_pos[0]-1, self.current_pos[1]],
                            [self.current_pos[0], self.current_pos[1]+1],
                            [self.current_pos[0], self.current_pos[1]-1]]

    ##            print("current: " + str(self.current_pos))
    ##            print("dir: " + str(self.direction))
    ##            print("goal: " + str(goal_pos))
    ##            print("achieved_pos: " + str(self.pos_achieved))
    ##            print("safe_pos: " + str(self.safe_pos))
    ##            print("path: " + str(self.path))
                
                if goal_pos in self.safe_pos:
    ##                print ("not go die")
                    if goal_pos not in self.pos_achieved:
                        return self.go_to(goal_pos)
                for pos in adjacent_pos:
                    if (pos in self.safe_pos and (pos not in self.pos_achieved)):
    ##                    print( "go to" + str(pos))
                        return self.go_to(pos)

    ##            if (self.direction != self.temp_dir):
    ##                print ("changing direction from" + str(self.temp_dir))
    ##                self.change_direction(Agent.Action.TURN_LEFT)
    ##                return Agent.Action.TURN_LEFT
                    
                
                else:
    ##                print ("go die")
    ##                if goal_pos not in self.pos_achieved :
    ##                    self.pos_achieved.append(goal_pos)

                    self.set_go_back_dir()
                    
                    if len(self.path) <= 1:
                        return self.go_to(self.path[0])
                    if (self.isgoing == False):
                        self.path.pop()
       
    ##                print("last path" + str(self.path[-1]))
                    return self.go_to(self.path[-1])

        else:
            if stench:
                self.spos.append(self.current_pos)
            if breeze:
                self.bpos.append(self.current_pos)
            
            goal_pos = self.update_pos()
            adjacent_pos = [[self.current_pos[0]+1, self.current_pos[1]],
                        [self.current_pos[0]-1, self.current_pos[1]],
                        [self.current_pos[0], self.current_pos[1]+1],
                        [self.current_pos[0], self.current_pos[1]-1]]

##            print("current: " + str(self.current_pos))
##            print("dir: " + str(self.direction))
##            print("goal: " + str(goal_pos))
##            print("achieved_pos: " + str(self.pos_achieved))
##            print("safe_pos: " + str(self.safe_pos))
##            print("path: " + str(self.path))
            
            if goal_pos in self.safe_pos:
##                print ("not go die")
                if goal_pos not in self.pos_achieved:
                    return self.go_to(goal_pos)
            for pos in adjacent_pos:
                if (pos in self.safe_pos and (pos not in self.pos_achieved)):
##                    print( "go to" + str(pos))
                    return self.go_to(pos)

##            if (self.direction != self.temp_dir):
##                print ("changing direction from" + str(self.temp_dir))
##                self.change_direction(Agent.Action.TURN_LEFT)
##                return Agent.Action.TURN_LEFT
                
            
            else:
##                print ("go die")
##                if goal_pos not in self.pos_achieved :
##                    self.pos_achieved.append(goal_pos)

                self.set_go_back_dir()
                
                if len(self.path) <= 1:
                    return self.go_to(self.path[0])
                if (self.isgoing == False):
                    self.path.pop()
   
##                print("last path" + str(self.path[-1]))
                return self.go_to(self.path[-1])


                
            

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def is_safe(self, stench, breeze):
        if stench or breeze:
            return False
        return True

    def change_direction(self, move):
        if move == Agent.Action.TURN_LEFT:
            self.direction += 1
            if self.direction > 4:  #if face to down, change direction to right
                self.direction = 1
        elif move == Agent.Action.TURN_RIGHT:
            self.direction -= 1
            if self.direction < 1:  #if face to right, change direction to down
                self.direction = 4

    def update_pos(self):
        if (self.direction == 1):
            return [self.current_pos[0] + 1, self.current_pos[1]]
        elif (self.direction == 2):
            return [self.current_pos[0], self.current_pos[1] + 1]
        elif (self.direction == 3):
            return [self.current_pos[0] - 1, self.current_pos[1]]
        elif (self.direction == 4):
            return [self.current_pos[0], self.current_pos[1] - 1]

    def reset_pos(self):
        if (self.direction == 1):  #right boundary
            self.current_pos[0] -= 1
            self.pos_achieved.pop()
            self.safe_pos.pop()
            self.path.pop()
            self.world_size[0] = self.current_pos[0]
        elif (self.direction == 2): #top boundary
            self.current_pos[1] -= 1
            self.pos_achieved.pop()
            self.safe_pos.pop()
            self.path.pop()
            self.world_size[1] = self.current_pos[1]
        elif (self.direction == 3): #left boundary
            self.current_pos[0] += 1
            self.pos_achieved.pop()
            self.safe_pos.pop()
            self.path.pop()
        elif (self.direction == 4): #bottom boundary
            self.current_pos[1] += 1
            self.pos_achieved.pop()
            self.safe_pos.pop()
            self.path.pop()

    def set_go_back_dir(self):
        if (self.direction == 1):
            self.temp_dir = 3
        elif (self.direction == 2):
            self.temp_dir = 4
        elif (self.direction == 3):
            self.temp_dir = 1
        elif (self.direction == 4):
            self.temp_dir = 2

    def no_safe_pos(self):
        if len(self.safe_pos) < 1:
            return False
        for pos in self.safe_pos:
            if pos not in self.pos_achieved:
                return False   
        return True

    def update_safe_pos(self):
        if (self.current_pos[0] > 0):  #left is not boundary
            temp1 = [self.current_pos[0]-1, self.current_pos[1]]
            if (temp1 not in self.safe_pos):
                self.safe_pos.append(temp1[:])
        if (self.current_pos[1] > 0):  #down is not boundary
            temp2 = [self.current_pos[0], self.current_pos[1]-1]
            if (temp2 not in self.safe_pos):
                self.safe_pos.append(temp2[:])

        temp3 = [self.current_pos[0]+1, self.current_pos[1]]
        if (temp3 not in self.safe_pos):
            self.safe_pos.append(temp3[:])
        temp4 = [self.current_pos[0], self.current_pos[1]+1]
        if (temp4 not in self.safe_pos):
            self.safe_pos.append(temp4[:])

        self.check_safe_pos()

    def check_safe_pos(self):
        if (self.world_size[0] != -1):
            for safe in self.safe_pos:
                if safe[0] > self.world_size[0]:
                    self.safe_pos.remove(safe)

        if (self.world_size[1] != -1):
            for safe in self.safe_pos:
                if safe[1] > self.world_size[1]:
                    self.safe_pos.remove(safe)

    def go_to(self, goal):
        self.isgoing = True
        if (goal[0] - self.current_pos[0]) != 0:  #go left or right
            if (goal[0] - self.current_pos[0]) > 0:  #should go right
                if self.direction == 1:
                    self.current_pos[0] += 1
                    if self.current_pos not in self.pos_achieved:
                        self.pos_achieved.append(self.current_pos[:])
##                    self.path.append(self.current_pos[:])
                    if (self.current_pos[:] != self.path[-1]):
                        self.path.append(self.current_pos[:])
##                    if (self.current_pos[:] not in self.path):
##                        self.path.append(self.current_pos[:])
                    self.isgoing = False
                    return Agent.Action.FORWARD
                else:
                    if self.direction == 4:
                        self.direction = 1
                        return Agent.Action.TURN_LEFT
                    else:
                        self.direction -= 1
                        return Agent.Action.TURN_RIGHT
            elif (goal[0] - self.current_pos[0]) < 0:  #should go left
                if self.direction == 3:
                    self.current_pos[0] -= 1
                    if self.current_pos not in self.pos_achieved:
                        self.pos_achieved.append(self.current_pos[:])
##                    self.path.append(self.current_pos[:])
                    if (self.current_pos[:] != self.path[-1]):
                        self.path.append(self.current_pos[:])                    
##                    if (self.current_pos[:] not in self.path):
##                        self.path.append(self.current_pos[:])
                    self.isgoing = False
                    return Agent.Action.FORWARD
                else:
                    if self.direction == 4:
                        self.direction -= 1
                        return Agent.Action.TURN_RIGHT
                    else:
                        self.direction += 1
                        return Agent.Action.TURN_LEFT
        elif (goal[1] - self.current_pos[1]) != 0:  #go top or down
            if (goal[1] - self.current_pos[1]) > 0:  #should go up
                if self.direction == 2:
                    self.current_pos[1] += 1
                    if self.current_pos not in self.pos_achieved:
                        self.pos_achieved.append(self.current_pos[:])
##                    self.path.append(self.current_pos[:])
                    if (self.current_pos[:] != self.path[-1]):
                        self.path.append(self.current_pos[:])
##                    if (self.current_pos[:] not in self.path):
##                        self.path.append(self.current_pos[:])
                    self.isgoing = False
                    return Agent.Action.FORWARD
                else:
                    if self.direction == 1:
                        self.direction += 1
                        return Agent.Action.TURN_LEFT
                    else:
                        self.direction -= 1
                        return Agent.Action.TURN_RIGHT
            elif (goal[1] - self.current_pos[1]) < 0:  #should go down
                if self.direction == 4:
                    self.current_pos[1] -= 1
                    if self.current_pos not in self.pos_achieved:
                        self.pos_achieved.append(self.current_pos[:])
##                    self.path.append(self.current_pos[:])
                    if (self.current_pos[:] != self.path[-1]):
                        self.path.append(self.current_pos[:])                    
##                    if (self.current_pos[:] not in self.path):
##                        self.path.append(self.current_pos[:])
                    self.isgoing = False
                    return Agent.Action.FORWARD
                else:
                    if self.direction == 1:
                        self.direction = 4
                        return Agent.Action.TURN_RIGHT
                    else:
                        self.direction += 1
                        return Agent.Action.TURN_LEFT
        
    def go_home(self):
        try:
            if (self.path[-2] == self.current_pos):
                self.path.pop()
            if (self.path[-2][0] - self.current_pos[0]) != 0:  #go left or right
                if (self.path[-2][0] - self.current_pos[0]) > 0:  #should go right
                    if self.direction == 1:
                        self.path.pop()
                        self.current_pos[0] += 1
                        return Agent.Action.FORWARD
                    else:
                        if self.direction == 4:
                            self.direction = 1
                            return Agent.Action.TURN_LEFT
                        else:
                            self.direction -= 1
                            return Agent.Action.TURN_RIGHT
                elif (self.path[-2][0] - self.current_pos[0]) < 0:  #should go left
                    if self.direction == 3:
                        self.path.pop()
                        self.current_pos[0] -= 1
                        return Agent.Action.FORWARD
                    else:
                        if self.direction == 4:
                            self.direction -= 1
                            return Agent.Action.TURN_RIGHT
                        else:
                            self.direction += 1
                            return Agent.Action.TURN_LEFT
            elif (self.path[-2][1] - self.current_pos[1]) != 0:  #go top or down
                if (self.path[-2][1] - self.current_pos[1]) > 0:  #should go up
                    if self.direction == 2:
                        self.path.pop()
                        self.current_pos[1] += 1
                        return Agent.Action.FORWARD
                    else:
                        if self.direction == 1:
                            self.direction += 1
                            return Agent.Action.TURN_LEFT
                        else:
                            self.direction -= 1
                            return Agent.Action.TURN_RIGHT
                elif (self.path[-2][1] - self.current_pos[1]) < 0:  #should go down
                    if self.direction == 4:
                        self.path.pop()
                        self.current_pos[1] -= 1
                        return Agent.Action.FORWARD
                    else:
                        if self.direction == 1:
                            self.direction = 4
                            return Agent.Action.TURN_RIGHT
                        else:
                            self.direction += 1
                            return Agent.Action.TURN_LEFT
        except:
            return Agent.Action.CLIMB
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
