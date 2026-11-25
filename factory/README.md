# 规则文件开发说明

这里是规则文件的生成车间，欢迎访问。


## 规则模板

`template/` 目录下为规则模板，`build_confs.py` 脚本运行时会按照模板生成规则文件。

每个规则对应一个模板，不过 `sr_head.txt` 和 `sr_foot.txt` 是例外，这两个文件是所有模板的公共的头部和尾部。


## 手工配置的文件

**manual_direct.txt**

列表，手动编写。记录走直连的域名或 IP。

**manual_proxy.txt**

列表，手动编写。记录走代理的域名或 IP。

**manual_reject.txt**

列表，手动编写。记录需要屏蔽的域名或 IP。

**manual_ai.txt**

OpenAI / ChatGPT / Claude 的显式域名列表，仅供 `sr_cnip_ad_plus_dns` 使用，生成指向 `AI` 手动组的规则。该组在 `template/sr_head_dns.txt` 定义，使用 `policy-regex-filter=^(residen-|Band|US-Band)` 从客户端已导入的节点中筛选成员，只匹配 `residen-`、`Band` 或 `US-Band` 开头的名称，区分大小写。组内不添加 `PROXY` 或其他不匹配的候选，节点由用户手动选择。筛选条件随生成的远程配置发布，客户端更新配置即可获得，无需在手机上编辑正则。

该配置的 `{{manual_ai}}` 放在通用规则之前，`{{manual_proxy_plus_without_ai}}` 从 Plus 列表中排除重复的 AI 域名；其他配置继续使用原来的 `{{manual_proxy_plus}}`，策略不变。此处不使用其他核心的 `GEOSITE` 语法，也不保存私人节点或凭据。

## 代码及自动生成的文件

**resultant/top50_direct.list** 

域名列表，由 `top500.py` 自动生成。记录着前 50 网站中所有可直连网站的域名。

**resultant/top50_proxy.list** 

域名列表，由 `top500.py` 自动生成。记录着前 50 网站中无法直连网站的域名。

其中未包括含有 `google` 关键字的域名，并且首页请求时间大于 10 秒也视为无法直连。

**top500.py**

脚本，运行所需时间较长。自动爬取生成 `top500_*.list` 文件。

-----------------------------------

**resultant/ad.list**

广告列表，由 `ad.py` 自动生成。包括所有需要屏蔽的广告服务器的域名和 IP。

**ad.py**

脚本，从指定的 Adblock Rule 中提取广告服务器的域名和 IP 至 `ad.list` 文件。合并各来源后统一处理全域 `@@` 例外，按完整域名标签匹配。若父域屏蔽会覆盖已放行的子域，则略去该父域屏蔽，其他明确列出的兄弟域名仍可屏蔽。带路径、协议、端口或 `$domain` 等条件的例外无法用整域列表表达，生成时跳过。这些行为可在 `factory/` 下运行 `python3 test_ad.py` 离线核对。

-----------------------------------

**resultant/gfw.list**

每日从官方 `gfwlist/gfwlist` 下载 AutoProxy 列表，由 `gfwlist.py` 生成带策略的 Shadowrocket 规则。两份模板在手工规则和广告拦截之后、宽泛直连名单之前嵌入该文件。块内先匹配上游 `@@` 例外（DIRECT），再匹配代理条目。

域名锚点转换为域名后缀；裸主机名保守地限制为精确匹配。协议、路径、通配符和正则表达式保留为 URL 规则。HTTPS 路径规则依赖客户端能看到相应 URL。转换遇到不支持的语法会中止本次构建。旧手工 GFW 补充名单及第三方来源不参与现行发布。
