# VLA 特征通信

本术语表统一论文中编码表示与策略输入表示的称呼。

## Language

**联合学习的视觉前端（jointly learned visual frontend）**:
将图像映射到策略视觉输入表示的可学习路径，其特征提取、压缩与恢复共同优化。
_Avoid_: 将其中的学生塔与 codec 描述成各自独立优化后拼接的两个系统。

**策略视觉输入接口（policy visual-input interface）**:
原视觉路径向后续策略计算提供视觉表示的边界，规定该表示的形状、排列及含义。
_Avoid_: 与相机图像输入端或压缩码的传输边界混用。

**策略视觉 token（policy visual tokens）**:
策略在视觉输入接口处使用的向量表示，用于表达图像观测。
_Avoid_: 将所有中间特征或压缩码都笼统称为策略视觉 token。

**压缩码（compressed codes）**:
视觉信息经过压缩得到的离散表示，是恢复策略视觉 token 的依据。
_Avoid_: 与恢复后的策略视觉 token 混用。

**轻量视觉编码器（light vision encoder, $s$）**:
机器人上运行的视觉编码器，由原视觉塔蒸馏初始化，之后随前端一起训练。
_Avoid_: student tower、student trunk、distilled tower（正文不再使用；"distilled/student" 只在说明初始化方式时出现一次）。

**特征 codec（feature codec）**:
机器人上把编码器特征变成整数码流的部分：特征头 $h$、量化 $Q$、时间编码与 rANS；云端有对应的熵解码与时间解码。
_Avoid_: 用 feature encoder 单独指代整个 codec。

**token 解码器（token decoder, $g_s$）**:
云端把压缩码直接恢复为策略视觉 token 的网络，即学习压缩里的 synthesis transform。
_Avoid_: feature decoder。
