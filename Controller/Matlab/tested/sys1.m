function xdot = sys1(t,x)
xdot = zeros(2,1);
theta = x(1);
dtheta = x(2);

g = 9.8;  % m/s^2
mc = 1;  % kg
m = 0.1;  % kg
L = 0.5;  % m
lambda = 5;
c=5;


F = (g * sin(theta) - m * L * dtheta^2 * cos(theta) * sin(theta)/(mc + m))/(L * ((4/3) - m * (cos(theta))^2/(mc + m))) ;
G =  (cos(theta)/(mc + m))/(L * (((4/3) - m*(cos(theta))^2/(mc + m)) ));

s =2*lambda -lambda * theta - dtheta;

u = 1/G * (-F + -c*dtheta + lambda * sign(s));

xdot(1) = dtheta;
xdot(2) = F + G*u;

end