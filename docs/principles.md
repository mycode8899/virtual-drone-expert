# 技术背景与参考出处

本文档说明「虚拟无人机跟拍」这一视觉范式从哪来、公开报道说了什么，以及本专家**为什么只是风格借鉴而不是技术复刻**。

---

## 1. Reality View 是什么

2026 年 11 月 21 日起，特斯拉向部分北美用户推送 FSD v15，其中的 **Reality View** 用车端生成模型实时「画」出车辆上方虚拟相机视角的逼真画面，取代了旧版的抽象线框与简化 3D 模型。由于观感接近开放世界游戏，车主与媒体大量使用「像 GTA6」「GTA 6 in real life」来形容它。

关键点是：画面**不是**多路摄像头拼接、**不是**游戏引擎渲染，而是模型在理解三维空间关系后重新生成像素。因此它可以给出物理摄像头拍不到的俯视 / 后方跟随视角，也能把驾驶意图（转向箭头、停车图钉）直接画进画面。

## 2. 公开报道提到的技术细节

> 以下是**媒体报道与厂商口径**，不是经独立复现验证的技术规格。不同报道对底层方法的描述并不完全一致，请按「据报道」理解。

| 项目 | 报道口径 | 出处 |
| --- | --- | --- |
| 生成支路规模 | 约 10 亿（1B）参数 | [新浪汽车](https://auto.sina.cn/2026-11-23/detail-inizsuwk8386422.d.html)、[PCM](https://www.pcmarket.com.hk/tesla-fsd-v15-reality-view-looks-as-gta/) |
| 模型类型 | 扩散 / 条件均值流（MeanFlow）；马斯克在 X 上称其为「缩小版世界模型 + 扩散模型」 | [腾讯新闻](https://news.qq.com/rain/a/20261124A0364Z00)、[TechRadar](https://www.techradar.com/sg/vehicle-tech/hybrid-electric-vehicles/tesla-drivers-hail-new-reality-mode-update-a-virtual-drone-style-view-of-your-car-that-looks-like-gta-6-in-real-life) |
| 另一套说法 | 部分中文报道称底座为「生成式高斯泼溅（GGS）」 | [新浪汽车](https://auto.sina.cn/2026-11-24/detail-inizuaru8073401.d.html) |
| 输入 | 全车摄像头 → 通用视觉编码器（UVE）特征，一路给驾驶决策、一路给可视化生成 | [新浪汽车](https://auto.sina.cn/2026-11-23/detail-inizsuwk8386422.d.html) |
| 时序生成 | 对上一轮生成画面加噪后去噪；每次生成 8 帧 / 36 fps，UVE 以 18 Hz 更新 | [腾讯新闻](https://news.qq.com/rain/a/20261124A0364Z00) |
| 时延 | 约 220 ms；厂商称通过在扩散 Transformer 中间层注入新特征可再降约 35% | [Skyline Wire](https://skylinewire.com/articles/tesla-fsd-v15-reality-view-features-hardware-limits-and-rollout) |
| 算力 | AI4 上约半个 TRIP 加速器，渲染与驾驶共享上游特征 | [游民星空](https://www.gamersky.com/news/202611/2251357.shtml) |
| 已知缺陷 | 交通标识文字在移动中出现纹理漂移 / 形变；存在输入延迟 | [腾讯新闻](https://news.qq.com/rain/a/20261124A08MTL00) |
| 可用范围 | 仅 HW4 / AI4 车型，北美早期体验用户 | [TechRadar](https://www.techradar.com/sg/vehicle-tech/hybrid-electric-vehicles/tesla-drivers-hail-new-reality-mode-update-a-virtual-drone-style-view-of-your-car-that-looks-like-gta-6-in-real-life) |

**关于口径冲突**：「扩散 / MeanFlow」与「生成式高斯泼溅」两类描述同时出现在同期报道中，可能对应不同层级（车端生成支路 vs 云端世界模拟器）或不同信源的理解偏差。本项目不对此下结论，仅把它们作为背景资料列出。

**关于原提示词的归因**：最初版本的 Agent 提示词把这套技术解析归给某位个人。该归因在可检索的公开资料中未能核实，因此本版本已移除具体人名，改为「公开报道与社区解读」，并把可核查的链接集中在本文件。

## 3. 与本专家的根本差异

| | Tesla Reality View | 本专家 |
| --- | --- | --- |
| 输入 | 多摄像头**实时**视频流 + 车辆状态 | **单条离线**视频 |
| 目标 | 可视化系统「理解到的世界」，服务驾驶信任 | 创作一段好看的镜头 |
| 几何约束 | 由多视角 + 时序连续性约束 | 基本没有，靠模型先验补全 |
| 输出性质 | 感知 / 规划结果的可视化 | 艺术化重构 |
| 运行位置 | 车端 AI4 芯片 | 宿主平台的云端视频模型 |

一句话：**输入信息量差了几个数量级**。单目视频里被遮挡的背面、路面纹理、远处建筑，模型只能「猜」，不可能还原。所以本专家的表现更接近「以原视频为参考的风格化重拍」，而不是「换机位重放」。

这也解释了常见现象：主体越清晰、背景越简单、镜头运动越平缓，成片越稳；反之容易出现主体形变、背景闪烁、镜头抖动。

## 4. 为什么仍值得做

- **镜头语言可迁移**。后方跟随、缓慢拉升、俯视环绕这些范式本身与实现无关，用提示词描述就能让通用视频模型产出可用的创意素材。
- **成本极低**。不需要多摄像头标定、深度估计、NeRF / 3DGS 重建管线。
- **可迭代**。一句话改高度、速度、焦段感就能重出，适合分镜预演与社交媒体内容。

## 5. 参考链接

- TechRadar — [Tesla drivers hail new 'Reality Mode' update … 'GTA 6 in real life'](https://www.techradar.com/sg/vehicle-tech/hybrid-electric-vehicles/tesla-drivers-hail-new-reality-mode-update-a-virtual-drone-style-view-of-your-car-that-looks-like-gta-6-in-real-life)
- Skyline Wire — [Tesla FSD v15: Reality View Features, Hardware Limits and Rollout](https://skylinewire.com/articles/tesla-fsd-v15-reality-view-features-hardware-limits-and-rollout)
- PCM 电脑广场 — [Tesla FSD 15「Reality View」畫面逼真如玩《GTA》](https://www.pcmarket.com.hk/tesla-fsd-v15-reality-view-looks-as-gta/)
- 新浪汽车 — [特斯拉 FSD 的 Reality View 画面究竟是如何实时生成的？](https://auto.sina.cn/2026-11-23/detail-inizsuwk8386422.d.html)
- 新浪汽车 — [Tesla Reality View 实景界面是什么样的？](https://auto.sina.cn/2026-11-24/detail-inizuaru8073401.d.html)
- 腾讯新闻 — [FSD V15：8 帧 36fps 实时生成，半个 TRIP 撑起 Reality View](https://news.qq.com/rain/a/20261124A0364Z00)
- 腾讯新闻 — [四大工程秘密：FSD V15 如何实现 Reality View？](https://news.qq.com/rain/a/20261124A08MTL00)
- 游民星空 — [GTA6 即视感！特斯拉新功能实景图爆火](https://www.gamersky.com/news/202611/2251357.shtml)

> 链接为 2026-11 的公开报道，内容可能更新或被修订；请以权利人 / 厂商的正式发布为准。
