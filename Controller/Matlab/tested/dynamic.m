clc;
clear;
close all;


t = 1:0.1:10;
x0 = [0.1 ,0];
[t ,x] = ode45('sys1',t,x0);

figure(1)
subplot(2,1,1)
plot(t,x(:,1),'b')

subplot(2,1,2)
plot(t,x(:,2),'b')

