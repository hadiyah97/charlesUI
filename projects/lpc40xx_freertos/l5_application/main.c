#include <stdio.h>
#include <stdlib.h>

#include "FreeRTOS.h"
#include "task.h"

#include "adc.h"
#include "gpio.h"
#include "pwm1.h"
#include "queue.h"
#include "semphr.h"
#include "uart.h"

SemaphoreHandle_t state_sem;
static QueueHandle_t rx_q, tx_q;

typedef enum {
  STOP = 0,
  FORWARD,
  BACKWARD,
  LEFT,
  RIGHT,
  F_LEFT,
  B_LEFT,
  F_RIGHT,
  B_RIGHT,
  CLOCKWISE,
  ANTICLOCKWISE
} move_state;

move_state state = STOP;
move_state lastState = STOP;
uint8_t speed = 0;

gpio_s dir0, dir1, dir2, dir3, pwm0, pwm1, pwm2, pwm3, us0, tx, rx;

char readVal;

void motor_task(void *params);
void demo_motor_task(void *params);
void cycle_state_task(void *params);
void ultrasonic_task(void *params);
void uart_test_task(void *params);

int main(void) {

  state_sem = xSemaphoreCreateBinary();

  rx_q = xQueueCreate(15, sizeof(char));
  tx_q = xQueueCreate(15, sizeof(char));

  xTaskCreate(uart_test_task, "uart test task", (4096 / sizeof(void *)), NULL, 2, NULL);

  xTaskCreate(motor_task, "motor task", (4096 / sizeof(void *)), NULL, 1, NULL);
  // xTaskCreate(cycle_state_task, "state task", (4096 / sizeof(void *)), NULL, 2, NULL);
  // xTaskCreate(demo_motor_task, "demo motor task", (4096 / sizeof(void *)), NULL, 1, NULL);

  printf("Created Task, Starting Scheduler\n");
  vTaskStartScheduler();

  return -1;
}

void uart_test_task(void *params) {
  tx = gpio__construct_with_function(GPIO__PORT_0, 0, 2);
  rx = gpio__construct_with_function(GPIO__PORT_0, 1, 2);

  const uint32_t pclkspeed = clock__get_core_clock_hz();
  uart__init(UART__3, pclkspeed, 115200);

  uart__enable_queues(UART__3, rx_q, tx_q);

  while (1) {
    printf("\n");

    if (xQueueReceive(rx_q, &readVal, portMAX_DELAY)) {
      // printf("%c\n", readVal);
      state = (readVal - '0');
      xSemaphoreGive(state_sem);
      // printf("state = %d\n", state);
    }

    // bool stat = uart__polled_get(UART__3, &readVal);
    // printf("stat: %d \n", stat);

    //   if (stat == 0) {
    //     for (int i = 0; i < 15; i++) {
    //       printf("%c", rx_q[i]);
    //     }
    //     printf("\n");
    //   }
    //   vTaskDelay(500);
  }
}

void motor_task(void *params) {

  // initialize PWM and direction pins for each motor
  pwm0 = gpio__construct_with_function(GPIO__PORT_2, 0, 1);
  pwm1 = gpio__construct_with_function(GPIO__PORT_2, 1, 1);
  pwm2 = gpio__construct_with_function(GPIO__PORT_2, 2, 1);
  pwm3 = gpio__construct_with_function(GPIO__PORT_2, 4, 1);

  dir0 = gpio__construct_with_function(GPIO__PORT_2, 5, 0);
  dir1 = gpio__construct_with_function(GPIO__PORT_2, 6, 0);
  dir2 = gpio__construct_with_function(GPIO__PORT_2, 7, 0);
  dir3 = gpio__construct_with_function(GPIO__PORT_2, 8, 0);

  gpio__set_as_output(dir0);
  gpio__set_as_output(dir1);
  gpio__set_as_output(dir2);
  gpio__set_as_output(dir3);

  // initialize pwm module
  pwm1__init_single_edge(1000);

  speed = 40;

  while (1) {

    if (xSemaphoreTake(state_sem, 0)) {

      pwm1__set_duty_cycle(PWM1__2_0, 0);
      pwm1__set_duty_cycle(PWM1__2_1, 0);
      pwm1__set_duty_cycle(PWM1__2_2, 0);
      pwm1__set_duty_cycle(PWM1__2_4, 0);
      vTaskDelay(200);

      switch (state) {
      case FORWARD: // 1111
        fprintf(stderr, "FORWARD\n");

        gpio__set(dir0);
        gpio__set(dir1);
        gpio__set(dir2);
        gpio__set(dir3);

        pwm1__set_duty_cycle(PWM1__2_0, speed);
        pwm1__set_duty_cycle(PWM1__2_1, speed);
        pwm1__set_duty_cycle(PWM1__2_2, speed);
        pwm1__set_duty_cycle(PWM1__2_4, speed);

        break;
      case BACKWARD: // 0000
        fprintf(stderr, "BACKWARD\n");

        gpio__reset(dir0);
        gpio__reset(dir1);
        gpio__reset(dir2);
        gpio__reset(dir3);

        pwm1__set_duty_cycle(PWM1__2_0, speed);
        pwm1__set_duty_cycle(PWM1__2_1, speed);
        pwm1__set_duty_cycle(PWM1__2_2, speed);
        pwm1__set_duty_cycle(PWM1__2_4, speed);

        break;
      case LEFT: // 0101
        fprintf(stderr, "LEFT\n");

        gpio__reset(dir0);
        gpio__set(dir1);
        gpio__reset(dir2);
        gpio__set(dir3);

        pwm1__set_duty_cycle(PWM1__2_0, speed);
        pwm1__set_duty_cycle(PWM1__2_1, speed);
        pwm1__set_duty_cycle(PWM1__2_2, speed);
        pwm1__set_duty_cycle(PWM1__2_4, speed);

        break;
      case RIGHT: // 1010
        fprintf(stderr, "RIGHT\n");

        gpio__set(dir0);
        gpio__reset(dir1);
        gpio__set(dir2);
        gpio__reset(dir3);

        pwm1__set_duty_cycle(PWM1__2_0, speed);
        pwm1__set_duty_cycle(PWM1__2_1, speed);
        pwm1__set_duty_cycle(PWM1__2_2, speed);
        pwm1__set_duty_cycle(PWM1__2_4, speed);

        break;
      case F_LEFT: // X1X1
        fprintf(stderr, "F_LEFT\n");

        gpio__set(dir1);
        gpio__set(dir3);

        pwm1__set_duty_cycle(PWM1__2_0, 0);
        pwm1__set_duty_cycle(PWM1__2_1, speed);
        pwm1__set_duty_cycle(PWM1__2_2, 0);
        pwm1__set_duty_cycle(PWM1__2_4, speed);

        break;
      case F_RIGHT: // 1X1X
        fprintf(stderr, "F_RIGHT\n");

        gpio__set(dir0);
        gpio__set(dir2);

        pwm1__set_duty_cycle(PWM1__2_0, speed);
        pwm1__set_duty_cycle(PWM1__2_1, 0);
        pwm1__set_duty_cycle(PWM1__2_2, speed);
        pwm1__set_duty_cycle(PWM1__2_4, 0);

        break;
      case B_LEFT: // 0X0X
        fprintf(stderr, "B_LEFT\n");

        gpio__reset(dir0);
        gpio__reset(dir2);

        pwm1__set_duty_cycle(PWM1__2_0, speed);
        pwm1__set_duty_cycle(PWM1__2_1, 0);
        pwm1__set_duty_cycle(PWM1__2_2, speed);
        pwm1__set_duty_cycle(PWM1__2_4, 0);

        break;
      case B_RIGHT: // X0X0
        fprintf(stderr, "B_RIGHT\n");

        gpio__reset(dir1);
        gpio__reset(dir3);

        pwm1__set_duty_cycle(PWM1__2_0, 0);
        pwm1__set_duty_cycle(PWM1__2_1, speed);
        pwm1__set_duty_cycle(PWM1__2_2, 0);
        pwm1__set_duty_cycle(PWM1__2_4, speed);

        break;
      case CLOCKWISE: // 1001
        fprintf(stderr, "CLOCKWISE\n");

        gpio__set(dir0);
        gpio__reset(dir1);
        gpio__reset(dir2);
        gpio__set(dir3);

        pwm1__set_duty_cycle(PWM1__2_0, speed);
        pwm1__set_duty_cycle(PWM1__2_1, speed);
        pwm1__set_duty_cycle(PWM1__2_2, speed);
        pwm1__set_duty_cycle(PWM1__2_4, speed);

        break;
      case ANTICLOCKWISE: // 0110
        fprintf(stderr, "ANTICLOCKWISE\n");

        gpio__reset(dir0);
        gpio__set(dir1);
        gpio__set(dir2);
        gpio__reset(dir3);

        pwm1__set_duty_cycle(PWM1__2_0, speed);
        pwm1__set_duty_cycle(PWM1__2_1, speed);
        pwm1__set_duty_cycle(PWM1__2_2, speed);
        pwm1__set_duty_cycle(PWM1__2_4, speed);

        break;
      case STOP:
        pwm1__set_duty_cycle(PWM1__2_0, 0);
        pwm1__set_duty_cycle(PWM1__2_1, 0);
        pwm1__set_duty_cycle(PWM1__2_2, 0);
        pwm1__set_duty_cycle(PWM1__2_4, 0);
        // vTaskDelay(200);
        fprintf(stderr, "STOP\n");
        break;
      default:
        break;
      }
    }
  }
}

void cycle_state_task(void *params) {
  while (1) {
    for (int i = 0; i < 20; i++) {
      if (i % 2 == 0) {
        lastState = state;
        state = STOP;
      } else if (i % 2 == 1) {
        state = lastState;
        state++;
      }
      xSemaphoreGive(state_sem);
      vTaskDelay(2000);
    }
    state = STOP;
    xSemaphoreGive(state_sem);
    vTaskDelay(2000);
  }
}

void demo_motor_task(void *params) {

  pwm1__init_single_edge(1000);

  printf("Done with motor function setup, entering loop\n");

  while (1) {
    // forward ramp up
    gpio__set(dir0);

    printf("20%% duty\n");
    pwm1__set_duty_cycle(PWM1__2_5, 20);
    vTaskDelay(1500); // 1500ms

    printf("50%% duty\n");
    pwm1__set_duty_cycle(PWM1__2_5, 50);
    vTaskDelay(1500);

    printf("80%% duty\n");
    pwm1__set_duty_cycle(PWM1__2_5, 80);
    vTaskDelay(1500);

    // stop motor
    printf("0%% duty (stopped)\n");
    pwm1__set_duty_cycle(PWM1__2_5, 0);
    vTaskDelay(500);

    // reverse ramp up
    gpio__reset(dir0);

    printf("20%% duty\n");
    pwm1__set_duty_cycle(PWM1__2_5, 20);
    vTaskDelay(1500); // 1500ms

    printf("50%% duty\n");
    pwm1__set_duty_cycle(PWM1__2_5, 50);
    vTaskDelay(1500);

    printf("80%% duty\n");
    pwm1__set_duty_cycle(PWM1__2_5, 80);
    vTaskDelay(1500);

    // stop motor
    printf("0%% duty (stopped)\n");
    pwm1__set_duty_cycle(PWM1__2_5, 0);
    vTaskDelay(500);
  }
}

void ultrasonic_task(void *params) {

  adc__initialize();
  us0 = gpio__construct_with_function(GPIO__PORT_1, 31, 3);
  uint16_t us_val = 0;

  while (1) {
    us_val = adc__get_adc_value(5);
    fprintf(stderr, "value: %d", us_val);
    vTaskDelay(500);
  }
}