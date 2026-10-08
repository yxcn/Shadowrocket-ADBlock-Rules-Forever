# 国内服务 DNS 模块

模块文件：[domestic-dns.sgmodule](../modules/domestic-dns.sgmodule)。

订阅地址：`https://yxcn.github.io/Shadowrocket-ADBlock-Rules-Forever/modules/domestic-dns.sgmodule`。

当前 `sr_cnip_ad_plus_dns.conf` 主配置已集成社区国内域名集与阿里/腾讯直连 DNS。更新并启用该主配置、确认规则集和实际 DNS 日志正常后，可关闭本模块；模块保留供其他主配置或回退使用。本页列出的 24 个范围仅描述独立模块，主配置的社区名单覆盖范围不同。

## 用途与范围

为明确列出的国内服务指定阿里和腾讯 DNS-over-HTTPS，改善因解析器位置导致的 CDN 选择差异。模块使用 `[Host]` 的 `server:` DNS 服务器映射，不固定服务 IP；只给两个 DNS 服务端点添加直连规则，保留主配置的默认 DNS、广告过滤和服务连接分流。

| 服务 | 域名范围 |
|---|---|
| 抖音 | `douyin.com`、`douyinstatic.com`、`douyinpic.com`、`douyinvod.com` 及子域名 |
| 豆包 | `doubao.com` 及子域名 |
| 微信、企业微信、QQ、腾讯视频 | `qq.com`、`wxqcloud.qq.com.cn`、`qpic.cn`、`gtimg.cn`、`cdn-go.cn` 及子域名 |
| 元宝、混元 | `yuanbao.tencent.com`、`hunyuan.tencent.com` 及子域名 |
| 剪映 | `capcut.cn`、`lv.ulikecam.com` 及子域名；`jianying.com`、`www.jianying.com`、`lf3-s.vlabstatic.com`、`lf3-lv-buz.vlabstatic.com`、`p11-seeyou-cn.byteimg.com` |
| DeepSeek | `deepseek.com` 及子域名 |
| 国内千问、通义 | `qianwen.com`、`tongyi.com`、`tongyi.aliyun.com` 及子域名；`document-ai-public-prod.oss-cn-beijing.aliyuncs.com` |

共 24 个范围，根域名和通配子域名分开表示后为 42 条 Host 映射。域名策略会覆盖这些域名下的其他服务，不按 App 进程隔离。

CapCut 海外站点、ChatGPT、Claude、`qwen.ai` 不在名单中。剪映与 CapCut 共用的 `lv-api.ulikecam.com`、`lv-pc-api.ulikecam.com` 以及 `byteimg.com`、`ibyteimg.com`、`bytedance.com`、`alicdn.com` 等共享根域名也不加入。

DNS 服务器选择与连接分流是两件事。模块不会强制所有名单域名直连；服务是否走直连、代理或广告屏蔽，仍应查看主配置规则及实际连接日志。App 自带 DoH 或直接访问 IP 的流量可能不使用本模块。

## 安装与更新

1. Shadowrocket → 配置 → 模块 → `+`，输入上面的模块订阅地址并下载。
2. 确认 `Domestic-DNS` 已启用；主配置继续使用原来的配置文件。
3. 若 VPN 正在运行，断开重连后检查 DNS 和连接日志。
4. 后续模块内容更新后，在模块页面更新此模块；更新节点订阅或主配置不等于更新模块。不要为了更新本模块批量刷新其他配置。

本模块独立于 `factory/build_confs.py`，每日主配置构建不会重新生成它。模块发布随 `build` 分支的 Pages 部署；日常调整只编辑模块源文件。

## 验证与回退

在相同网络和相同节点下对照关闭/启用模块的 DNS 回答、解析耗时、实际服务请求，特别检查抖音资源、国内剪映与海外 CapCut 的边界。仅出现模块勾选不等于真实 DNS 请求已经采用国内解析器，DNS 改善也不等于完整 App 启动改善。

需要回退时关闭 `Domestic-DNS` 并重连 VPN；不需要更换主配置、节点或其他模块。
