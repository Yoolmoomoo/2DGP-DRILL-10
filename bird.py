from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font
from state_machine import *
import game_world
import game_framework
import random

# Bird Run Speed
PIXEL_PER_METER = (10.0/0.3) # 10 PIXEL PER 30CM
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

class Idle:
    @staticmethod
    def enter(bird, e):
        if start_event(e):
            bird.action = 3
            bird.face_dir = 1
        elif right_down(e) or left_up(e):
            bird.action = 2
            bird.face_dir = -1
        elif left_down(e) or right_up(e):
            bird.action = 3
            bird.face_dir = 1

        bird.frame = 0
        bird.wait_time = get_time()

    @staticmethod
    def exit(bird, e):
        if space_down(e):
            bird.fire_ball()

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        # bird.x += bird.dir * 5
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        if bird.x >= 1580:
            bird.dir = -1
        if bird. x <= 30:
            bird.dir = 1

    @staticmethod
    def draw(bird):
        if bird.dir == 1:
            bird.image.clip_composite_draw(int(bird.frame) * 182, 330, 182, 168,
                                       0, '', bird.x - 25, bird.y - 25, 100, 100)
        if bird.dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) * 182, 330, 182, 168,
                                           0, 'h', bird.x - 25, bird.y - 25, 100, 100)




class Sleep:
    @staticmethod
    def enter(bird, e):
        if start_event(e):
            bird.face_dir = 1
            bird.action = 3
        bird.frame = 0

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION*TIME_PER_ACTION*game_framework.frame_time) % 5


    @staticmethod
    def draw(bird):
        if bird.face_dir == 1:
            bird.image.clip_composite_draw(int(bird.frame) * 100, 300, 100, 100,
                                          3.141592 / 2, '', bird.x - 25, bird.y - 25, 100, 100)
        else:
            bird.image.clip_composite_draw(int(bird.frame) * 100, 200, 100, 100,
                                          -3.141592 / 2, '', bird.x + 25, bird.y - 25, 100, 100)


class Run:
    @staticmethod
    def enter(bird, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            bird.dir, bird.face_dir, bird.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            bird.dir, bird.face_dir, bird.action = -1, -1, 0

    @staticmethod
    def exit(bird, e):
        if space_down(e):
            bird.fire_ball()


    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 5
        # bird.x += bird.dir * 5
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(bird):
        bird.image.clip_draw(int(bird.frame) * 100, bird.action * 100, 100, 100, bird.x, bird.y)



class Bird:

    def __init__(self):
        self.x, self.y = random.randint(100, 1500), random.randint(200, 500)
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('bird_animation.png')
        # self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Idle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        # self.font.draw(self.x-60, self.y+50, f'(Time: {get_time():.2f})',(255,255,0))
