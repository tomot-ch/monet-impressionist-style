# Monet Impressionist Style · 莫奈印象派风格

[中文](#中文) · [English](#english)

## 中文

这是一个供 Codex 使用的图像创作 skill：根据文字生成画面，或把照片转绘为**保留原场景、以光色和笔触为核心的莫奈式印象派作品**。它不是一键油画滤镜。处理照片时，原图决定构图、物体位置和实际光线；精选的绘画局部切片只用于指导色彩关系、笔触和边缘处理。

### 三步快速使用

1. 在 Codex 中说：

   > 请用 `$skill-installer` 安装这个 GitHub skill：`https://github.com/tomot-ch/monet-impressionist-style`

   也可以手动安装到个人技能目录：

   ```bash
   mkdir -p "$HOME/.agents/skills"
   git clone https://github.com/tomot-ch/monet-impressionist-style.git "$HOME/.agents/skills/monet-impressionist-style"
   ```

2. 如果 Codex 没有立即识别新 skill，重启 Codex。确认当前环境有可用的图像生成或编辑工具；这个仓库提供创作流程和风格参考，本身不是独立的出图程序。
3. 上传照片，在对话中直接指定 skill 和强度。例如：

   > 用 `$monet-impressionist-style` 将这张照片转绘为莫奈式印象派作品，强度为**中等（balanced / 55）**。保留原图构图、主体位置和夕阳的真实明暗关系，输出 PNG。

   没有照片也可以从文字生成：

   > 用 `$monet-impressionist-style` 生成一幅清晨河岸与小船的印象派画面，强度为中等。

   多张照片请分别出图；如需保留某些细节、人物或建筑，请在请求中点明。

### 强度怎么选

| 强度 | 约定值 | 效果 |
| --- | ---: | --- |
| 轻（light） | 25 | 大体保留照片的色彩和明暗，只适度加入可见笔触与颜色分离。 |
| 中（balanced，默认） | 55 | 明显重绘色彩、光感和笔触，同时维持场景可辨识。 |
| 强（strong） | 80 | 更大胆地简化和重绘；让相邻物体的部分边缘通过笔触与空气感融合，但保留关键轮廓。 |

也可指定 0–100 的自定义强度。数值是给图像模型的**语义指导**，不是精确的滤镜参数。从 67 起会逐步加强物体之间的选择性边缘融合，不会把整幅画均匀模糊。

### 作品会如何处理

- **照片转绘：**尽量保持原图纵横比、取景、透视、主要轮廓、物体位置及原本的光照事件；默认输出 PNG。
- **文字生成：**默认使用 4:3 构图并输出 PNG。
- **风格依据：**优先观察瞬时自然光、彩色阴影、并置色彩和因材质而异的笔触；远看形成整体，近看可见局部色彩与笔触。
- **边界：**不默认生成深蓝、近乎抽象的晚期睡莲风格，也不以统一的厚涂纹理或柔焦替代印象派处理。实际效果取决于所用图像工具，建议检查生成图并针对具体区域提出修改。

### 仓库结构

| 路径 | 用途 |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Codex 的主工作流程：分析场景、选参考、生成、检查和修订。 |
| [`references/style-profile.md`](references/style-profile.md) | 风格目标、光色原则、强度及常见失败表现。 |
| [`references/technique-reading.md`](references/technique-reading.md) | 如何观察绘画局部，而不把参考图的物体直接复制进新画面。 |
| [`references/feedback-calibration.md`](references/feedback-calibration.md) | 输出偏差与针对性校准。 |
| [`references/technique-atlas.json`](references/technique-atlas.json) 和 [`assets/reference-slices/index.json`](assets/reference-slices/index.json) | 已分析的参考切片与检索索引。 |
| [`assets/reference-slices/`](assets/reference-slices/) | 供视觉参考的小尺寸绘画切片和主题板。 |
| [`references/reference-curation.md`](references/reference-curation.md) 和 [`scripts/build_reference_sets.py`](scripts/build_reference_sets.py) | 扩充参考素材时的整理规范与构建脚本；普通使用无需运行。 |

仓库只收录派生的参考切片和索引，不需要下载或上传大型 TIFF 原作。若要扩充素材，请先阅读整理规范，保留来源记录，并在使用图像时自行确认适用的权利与许可。

安装与调用方式以 [Codex 官方技能文档](https://developers.openai.com/zh-Hans/docs/build-skills) 为准。

## English

This is a Codex skill for creating an image from a text brief or restyling a photograph into a **recognizable, light-driven, Monet-inspired Impressionist scene**. It is not a one-click oil-paint filter. For photo restyling, the source image controls composition, object placement, and the actual lighting; curated painting crops guide color relationships, brushwork, and edge handling only.

### Quick start in three steps

1. Tell Codex:

   > Use `$skill-installer` to install this skill from GitHub: `https://github.com/tomot-ch/monet-impressionist-style`

   Or install it manually in your personal skills directory:

   ```bash
   mkdir -p "$HOME/.agents/skills"
   git clone https://github.com/tomot-ch/monet-impressionist-style.git "$HOME/.agents/skills/monet-impressionist-style"
   ```

2. Restart Codex if it does not detect the new skill immediately. Make sure an image generation or editing tool is available in your environment; this repository provides the workflow and references, not a standalone image-rendering application.
3. Attach a photo and invoke the skill in your prompt. For example:

   > Use `$monet-impressionist-style` to restyle this photo at **balanced strength (55)**. Preserve the framing, subject positions, and the sunset's actual light and shadow relationships. Output a PNG.

   For a new image without a photo:

   > Use `$monet-impressionist-style` to create a morning riverbank with a small boat, at balanced strength.

   Request one output per photo. Name any people, architecture, or other details that must remain especially clear.

### Choose a strength

| Strength | Guide value | Effect |
| --- | ---: | --- |
| Light | 25 | Mostly retain the source color and tonal modeling, adding modest visible strokes and color separation. |
| Balanced (default) | 55 | Actively reinterpret color, light, and brushwork while keeping the scene recognizable. |
| Strong | 80 | Simplify and repaint more assertively; selectively merge edges between neighboring objects through strokes and atmosphere while retaining key contours. |

You can also specify a custom value from 0 to 100. These values are **semantic guidance** for the image model, not exact filter settings. From 67 upward, the skill progressively softens selected object-to-object boundaries; it does not apply uniform blur to the whole image.

### What to expect

- **Photo restyling:** preserve the source aspect ratio, framing, perspective, major silhouettes, object positions, and observed light event where possible; PNG by default.
- **Text-to-image generation:** 4:3 composition and PNG by default.
- **Visual approach:** transient natural light, colored shadows, juxtaposed color, and material-specific strokes that cohere at a distance and remain visible up close.
- **Boundaries:** no default dark-blue, near-abstract late water-lily treatment, uniform impasto filter, or soft focus masquerading as Impressionism. Results depend on the available image tool; inspect the output and request corrections to specific regions when needed.

### Repository map

| Path | Purpose |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Main Codex workflow: observe, select references, generate, inspect, revise. |
| [`references/style-profile.md`](references/style-profile.md) | Style target, lighting principles, strength, and failure conditions. |
| [`references/technique-reading.md`](references/technique-reading.md) | How to read painting crops without copying their depicted objects. |
| [`references/feedback-calibration.md`](references/feedback-calibration.md) | Output failure modes and targeted corrections. |
| [`references/technique-atlas.json`](references/technique-atlas.json) and [`assets/reference-slices/index.json`](assets/reference-slices/index.json) | Analyzed reference crops and lookup index. |
| [`assets/reference-slices/`](assets/reference-slices/) | Compact visual crops and subject boards. |
| [`references/reference-curation.md`](references/reference-curation.md) and [`scripts/build_reference_sets.py`](scripts/build_reference_sets.py) | Reference curation rules and build script; not needed for everyday use. |

The repository contains derived reference crops and indexes, not the large original TIFF paintings. If you extend the reference set, read the curation rules, retain provenance, and check the applicable rights and permissions for the images you use.

For installation and invocation details, see the [official Codex skills documentation](https://developers.openai.com/en-US/docs/build-skills).
