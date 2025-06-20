import numpy as np
import matplotlib.pyplot as plt
from control import tf, feedback, step_response

# 定义加热炉模型 (基于两点法辨识)
K = 9.9  # 增益 (℃/V)
T = 2154  # 时间常数 (s)
G = tf([K], [T, 1])  # 传递函数 G(s) = K / (T s + 1)

# PID参数 (优化后的值)
Kp = 12.5
Ki = 0.005
Kd = 4500
Ts = 0.5  # 采样时间 (s)

# 构造PID控制器 (连续形式，之后离散化)
PID = tf([Kd, Kp, Ki], [1, 0])  # PID控制器 s^2 + Kp*s + Ki 形式

# 闭环系统
system = feedback(PID * G, 1)  # 负反馈闭环

# 仿真时间
t = np.arange(0, 5000, Ts)

# 阶跃响应 (目标温度35℃，初始温度16.85℃)
t_step, y_step = step_response(system, T=t)
# 调整输出：从0到1的响应映射到16.85℃到35℃
y_temp = 16.85 + (35 - 16.85) * y_step  # 线性映射到实际温度

# 绘制结果
plt.plot(t, y_temp, label='Temperature')
plt.plot(t, 35 * np.ones_like(t), '--', label='Setpoint (35°C)')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.title('PID Controlled Temperature Response')
plt.legend()
plt.grid()
plt.show()
