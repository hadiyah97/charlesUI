#include <stdio.h>

#include "FreeRTOS.h"
#include "task.h"

#include "gpio.h"
#include "pwm1.h"

void motor_task(void *params);

gpio_s dir1 = {2, 7};
gpio_s dir2 = {2, 6};
gpio_s pwm = {2, 5};

int main(void) {

  xTaskCreate(motor_task, "motor task", (4096 / sizeof(void *)), NULL, 1, NULL);

  printf("Created Task, Starting Scheduler\n");
  vTaskStartScheduler();

  return -1;
}

void motor_task(void *params) {

  pwm1__init_single_edge(1000);

  gpio__set_function(dir1, 0);
  gpio__set_function(dir2, 0);
  gpio__set_function(pwm, 1);

  gpio__set_as_output(dir1);
  gpio__set_as_output(dir2);

  gpio__set(dir1);
  gpio__reset(dir2);

  printf("Done with motor function setup, entering loop\n");

  while (1) {
    printf("20%% duty\n");
    pwm1__set_duty_cycle(PWM1__2_5, 20);
    vTaskDelay(1500); // 1500ms

    printf("50%% duty\n");
    pwm1__set_duty_cycle(PWM1__2_5, 50);
    vTaskDelay(1500);

    printf("80%% duty\n");
    pwm1__set_duty_cycle(PWM1__2_5, 80);
    vTaskDelay(1500);
  }
}