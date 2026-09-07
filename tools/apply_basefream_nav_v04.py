from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css = r'''
/* BaseFream SimpleMenu navigation V0.4 */
.bfShell{grid-template-columns:210px minmax(0,1fr)!important}
.bfSider{position:sticky;top:62px;height:calc(100vh - 62px);padding:0!important;display:flex;flex-direction:column;overflow:hidden;background:linear-gradient(180deg,#EAF2FF 0%,#C0DDFD 100%)!important;border-right:0!important;box-shadow:1px 0 0 rgba(77,112,153,.08)}
.bfSiderTop{padding:14px 10px 10px}.bfOrgSwitch{height:52px;padding:0 12px;display:flex;align-items:center;gap:10px;border-radius:8px;color:#334155;background:rgba(255,255,255,.52);border:1px solid rgba(255,255,255,.5);cursor:default}.bfOrgSwitch:hover{background:rgba(255,255,255,.72)}
.bfOrgIcon{width:30px;height:30px;border-radius:7px;display:grid;place-items:center;flex:0 0 auto;background:#fff;color:#026AFF;box-shadow:0 2px 8px rgba(38,80,125,.08)}.bfOrgIcon svg{width:17px;height:17px}.bfOrgText{min-width:0;flex:1}.bfOrgText b{display:block;font-size:12px;line-height:18px;color:#1E293B;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.bfOrgText span{display:block;font-size:10px;color:#7A8AA0;line-height:15px}.bfOrgArrow{font-size:13px;color:#8B9AAD}
.bfMenuScroll{flex:1;overflow:auto;padding:2px 10px 10px;scrollbar-width:none}.bfMenuScroll::-webkit-scrollbar{display:none}.bfMenuGroup{padding:10px 14px 5px;font-size:11px;line-height:18px;color:#7E8FA5;letter-spacing:.04em}.bfMenu{display:block;width:100%;padding:0;margin:0;list-style:none;font-size:13px;color:rgba(0,0,0,.7)}
.bfMenuItem{position:relative;z-index:1;display:flex;align-items:center;min-height:44px;padding:11px 24px;margin-top:2px;border-top:2px solid transparent;border-bottom:2px solid transparent;background-clip:padding-box;border-radius:8px;list-style:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;cursor:pointer;color:rgba(0,0,0,.7);transition:all .2s ease-in-out}.bfMenuItem:hover{color:#0083FF;background:rgba(2,106,255,.10)}.bfMenuItem.on{color:#0083FF!important;background:#C7DEFF!important;font-weight:600}.bfMenuItemIcon{width:18px;height:18px;margin-right:8px;display:grid;place-items:center;flex:0 0 auto;color:currentColor}.bfMenuItemIcon svg{width:18px;height:18px}.bfMenuItemText{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.bfMenuItem.on:after{content:"";position:absolute;right:0;top:9px;bottom:9px;width:2px;border-radius:2px;background:#026AFF}
.bfSubPanel{margin:4px 10px 0;padding:10px 12px;border-radius:8px;background:rgba(255,255,255,.42);border:1px solid rgba(255,255,255,.38)}.bfSubPanelHead{display:flex;align-items:center;justify-content:space-between;gap:8px}.bfSubPanelId{font-size:10px;color:#74869D}.bfSubPanelTitle{font-size:12px;color:#334155;font-weight:600;margin-top:5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.bfSubPanel .pill{margin-top:7px;padding:3px 7px;font-size:10px}
.bfSiderFoot{padding:8px 10px 10px;border-top:1px solid rgba(89,119,153,.10)}.bfCollapse{height:36px;padding:0 12px;display:flex;align-items:center;gap:9px;border-radius:8px;color:#61758E;font-size:12px;cursor:pointer;transition:.2s}.bfCollapse:hover{background:rgba(255,255,255,.5);color:#026AFF}.bfCollapseIcon{width:18px;height:18px;display:grid;place-items:center;font-size:17px;transition:transform .2s}
.bfShell.bfCollapsed{grid-template-columns:64px minmax(0,1fr)!important}.bfShell.bfCollapsed .bfSiderTop{padding:14px 8px 10px}.bfShell.bfCollapsed .bfOrgSwitch{justify-content:center;padding:0}.bfShell.bfCollapsed .bfOrgText,.bfShell.bfCollapsed .bfOrgArrow,.bfShell.bfCollapsed .bfMenuGroup,.bfShell.bfCollapsed .bfMenuItemText,.bfShell.bfCollapsed .bfSubPanel,.bfShell.bfCollapsed .bfCollapse span{display:none}.bfShell.bfCollapsed .bfMenuScroll{padding-left:8px;padding-right:8px}.bfShell.bfCollapsed .bfMenuItem{justify-content:center;padding:11px 0}.bfShell.bfCollapsed .bfMenuItemIcon{margin-right:0}.bfShell.bfCollapsed .bfMenuItem.on:after{display:none}.bfShell.bfCollapsed .bfCollapse{justify-content:center;padding:0}.bfShell.bfCollapsed .bfCollapseIcon{transform:rotate(180deg)}
@media(max-width:980px){.bfShell{grid-template-columns:188px minmax(0,1fr)!important}.bfMenuItem{padding-left:18px;padding-right:18px}}
'''

if '/* BaseFream SimpleMenu navigation V0.4 */' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)

new_pc = r'''function pc(content){var r=role();var isGroup=r==='group';var n=isGroup?[['group-dashboard','运营驾驶舱','chart'],['group-trace','工单穿透','eye']]:[['work-center','工单中心','order'],['work-detail','工单详情','report'],['work-dispatch','受理派单','team']];var current=n.filter(function(x){return location.hash==='#'+x[0]})[0]||n[0];var nav=n.map(function(x){return '<li class="bfMenuItem '+(location.hash==='#'+x[0]?'on':'')+'" onclick="go(\\''+x[0]+'\\')"><span class="bfMenuItemIcon">'+icon(x[2])+'</span><span class="bfMenuItemText">'+x[1]+'</span></li>'}).join('');var org=isGroup?'蓝投集团运营管理中心':'蓝海嘉园物业服务中心';var orgType=isGroup?'集团监管':'物业运营';return top('<div class="shell bfShell"><aside class="sidebar bfSider"><div class="bfSiderTop"><div class="bfOrgSwitch"><span class="bfOrgIcon">'+icon(isGroup?'chart':'home')+'</span><div class="bfOrgText"><b>'+org+'</b><span>'+orgType+'</span></div><span class="bfOrgArrow">⌄</span></div></div><div class="bfMenuScroll"><div class="bfMenuGroup">业务导航</div><ul class="bfMenu">'+nav+'</ul><div class="bfMenuGroup">演示工单</div><div class="bfSubPanel"><div class="bfSubPanelHead"><span class="bfSubPanelId">'+D.id+'</span></div><div class="bfSubPanelTitle">公共区域漏水</div><span class="pill '+(D.state===0?'orange':D.state>=5?'green':'')+'">'+statusNames[D.state]+'</span></div></div><div class="bfSiderFoot"><div class="bfCollapse" onclick="togglePcSider()"><b class="bfCollapseIcon">‹</b><span>收起菜单</span></div></div></aside><section class="workspace"><div class="multiTabs"><span class="pcTab">首页</span><span class="pcTab on">'+current[1]+'</span><span class="tabTools">×</span></div><main class="main">'+content+'</main></section></div>')}function phone(content){'''

pat = re.compile(r'function pc\(content\)\{.*?\}\s*function phone\(content\)\{', re.S)
s, count = pat.subn(new_pc, s, count=1)
if count != 1:
    raise SystemExit(f'pc function replace failed: {count}')

marker = "window.go=go;window.setState=setState;window.resetDemo=resetDemo;"
insert = "function togglePcSider(){var sh=document.querySelector('.bfShell');if(sh)sh.classList.toggle('bfCollapsed')}window.togglePcSider=togglePcSider;"
if insert not in s:
    s = s.replace(marker, marker + insert, 1)

s = s.replace('蓝投一码呼 V0.3 演示原型', '蓝投一码呼 V0.4 演示原型', 1)
s = s.replace('蓝投一码呼 · V0.3', '蓝投一码呼 · V0.4')
s = s.replace('社区居民服务演示原型 V0.3', '社区居民服务演示原型 V0.4')
p.write_text(s, encoding='utf-8')
