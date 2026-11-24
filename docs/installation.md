# 安装与使用

## 环境要求

- 支持导入本地专家包的 **WorkBuddy / CodeBuddy** 客户端。
- 宿主已接入**视频生成能力**（专家本身不提供模型）。若当前会话无法生成视频，专家只能给出镜头设计方案与提示词，无法产出成片。
- 本地打包需要 Python 3.8+（仅标准库，无第三方依赖）。

## 方式一：导入 zip（推荐）

1. 到 [Releases](../../releases) 下载 `virtual-drone-expert.zip`；或在仓库根目录执行：

   ```bash
   python scripts/build-package.py
   ```

   产物位于 `dist/virtual-drone-expert.zip`。

2. 打开客户端 → **专家** → 导入本地专家包 → 选择该 zip。
3. 在专家列表中找到「虚拟无人机拍摄专家 / Virtual Drone Shot Expert」，开始对话。

> zip 顶层目录必须是 `virtual-drone-expert/`，且 `.codebuddy-plugin/plugin.json` 位于该目录内。用 `scripts/build-package.py` 生成时会保证这一点；手工压缩时请勿把父目录一起打包进去。

## 方式二：直接放置目录

把仓库中的以下四个部分放进客户端的本地专家目录（具体路径以客户端版本为准）：

```
virtual-drone-expert/
├── .codebuddy-plugin/plugin.json
├── agents/virtual-drone-expert.md
├── avatars/expert.png
└── README.md
```

重启或刷新专家列表即可生效。`docs/`、`scripts/`、`.github/` 属于仓库资料，不是导入所必需。

## 方式三：从源码构建与校验

```bash
git clone https://github.com/mycode8899/virtual-drone-expert.git
cd virtual-drone-expert
python scripts/build-package.py
python scripts/build-package.py --check     # 只校验包结构，不写文件
```

校验会检查：`plugin.json` 是否为合法 JSON、必填字段是否齐全、`agents` 指向的文件是否存在、头像是否为有效 PNG、zip 顶层结构是否正确。

## 使用流程

1. **上传视频**。建议 3–15 秒、主体清晰、镜头运动平缓、分辨率不低于 720p。
2. **描述镜头**。说清风格 + 高度 / 距离 / 方位 / 速度中的任意几项即可，不必写满。示例见 [提示词示例](./prompt-examples.md)。
3. **确认方案**。专家会先给出场景理解与相机路径设计；这一步可以直接改参数。
4. **生成成片**。由宿主平台的视频模型完成。
5. **迭代**。针对「主体漂移 / 镜头抖 / 背景闪」等问题按专家给出的参数建议重出。

## `plugin.json` 字段说明

| 字段 | 作用 | 修改建议 |
| --- | --- | --- |
| `name` / `agentName` | 专家唯一标识 | **不要改**，是导入契约 |
| `agents` | Agent 提示词文件路径列表 | 新增提示词文件时才改 |
| `expertType` | 专家类型，固定 `agent` | 不要改 |
| `version` | 语义化版本，与 `CHANGELOG.md` / tag 保持一致 | 发版时递增 |
| `displayName` / `title` / `profession` | 专家中心显示的名称、头衔、职业 | 可改，需中英双语 |
| `displayDescription` / `description` | 卡片简介 / 详细描述 | 可改，避免暗示官方授权 |
| `categoryId` | 分类 ID（`04-DataAI`） | 按宿主分类表填写 |
| `tags` | 检索标签 | 可增删，保持中英双语 |
| `defaultInitPrompt` / `quickPrompts` | 开场白与快捷提示词 | 可自由扩充 |

> 不同客户端版本支持的字段可能不同。新增字段（如头像路径、主页链接）前请先确认宿主 schema，未知字段可能被忽略或导致校验失败。

## 自定义

- **改人设与语气**：编辑 `agents/virtual-drone-expert.md` 的「角色」与「语言风格」段。
- **加风格预设**：在「相机路径设计」段增加条目，并同步更新 `docs/prompt-examples.md`。
- **改快捷提示词**：编辑 `plugin.json` 的 `quickPrompts`。
- **换头像**：替换 `avatars/expert.png`（建议正方形、透明底、≤ 512×512），保持文件名不变。
- **做英文版**：复制 Agent 提示词翻译后，在 `agents` 数组中增加路径，或在提示词内加入语言切换规则。

## 卸载

在客户端专家列表中移除该专家即可；若用方式二，删除对应的 `virtual-drone-expert/` 目录。项目不写入注册表、不创建后台服务、不产生用户数据。

## 故障排查

| 现象 | 处理 |
| --- | --- |
| 专家列表里看不到 | 检查 zip 顶层目录结构；确认 `.codebuddy-plugin/` 未被系统隐藏或过滤 |
| 导入报元数据错误 | 用 `python -m json.tool .codebuddy-plugin/plugin.json` 验证 JSON |
| 头像不显示 | 确认 `avatars/expert.png` 存在且为有效 PNG |
| 能对话但不出视频 | 当前会话未接入视频生成能力，见 [FAQ](./faq.md) |
| 生成结果主体漂移 | 缩短时长、降低运动幅度、明确「保持主体外观一致」 |
