#include <stdio.h>

#include "FreeRTOS.h"
#include "task.h"

#include "gpio.h"
#include "pwm1.h"

gpio_s dir, pwm;

void motor_task(void *params);

int main(void) {
  dir = gpio__construct_with_function(GPIO__PORT_2, 6, 0);
  pwm = gpio__construct_with_function(GPIO__PORT_2, 5, 1);

  gpio__set_as_output(dir);

  xTaskCreate(motor_task, "motor task", (4096 / sizeof(void *)), NULL, 1, NULL);

  printf("Created Task, Starting Scheduler\n");
  vTaskStartScheduler();

  return -1;
}

void motor_task(void *params) {

  pwm1__init_single_edge(1000);

  printf("Done with motor function setup, entering loop\n");

  while (1) {
    // forward ramp up
    gpio__set(dir);

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
    gpio__reset(dir);

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