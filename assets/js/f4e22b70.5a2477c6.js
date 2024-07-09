"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[661],{7575:(e,o,t)=>{t.r(o),t.d(o,{assets:()=>a,contentTitle:()=>i,default:()=>v,frontMatter:()=>c,metadata:()=>d,toc:()=>r});var n=t(4848),s=t(8453);const c={sidebar_position:7},i="Voting",d={id:"commands/voting",title:"Voting",description:"In order to vote, you will require the list of active proposals, You can list them with:",source:"@site/docs/commands/07-voting.md",sourceDirName:"commands",slug:"/commands/voting",permalink:"/docs/commands/voting",draft:!1,unlisted:!1,editUrl:"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/docs/commands/07-voting.md",tags:[],version:"current",sidebarPosition:7,frontMatter:{sidebar_position:7},sidebar:"tutorialSidebar",previous:{title:"Proposals",permalink:"/docs/commands/proposal"}},a={},r=[{value:"Cast vote with drep keys",id:"cast-vote-with-drep-keys",level:3},{value:"examples:",id:"examples",level:3},{value:"Cast vote with cc keys",id:"cast-vote-with-cc-keys",level:3}];function l(e){const o={code:"code",h1:"h1",h3:"h3",p:"p",pre:"pre",strong:"strong",...(0,s.R)(),...e.components};return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(o.h1,{id:"voting",children:"Voting"}),"\n",(0,n.jsx)(o.p,{children:"In order to vote, you will require the list of active proposals, You can list them with:"}),"\n",(0,n.jsx)(o.pre,{children:(0,n.jsx)(o.code,{children:"gov-cli ls\n\n"})}),"\n",(0,n.jsxs)(o.p,{children:[(0,n.jsx)(o.strong,{children:"Governance action id format"}),": ",(0,n.jsx)(o.code,{children:"proposedTxHash#index"}),"."]}),"\n",(0,n.jsx)(o.h3,{id:"cast-vote-with-drep-keys",children:"Cast vote with drep keys"}),"\n",(0,n.jsx)(o.pre,{children:(0,n.jsx)(o.code,{children:"gov-cli drep vote <gov_action> [yes|no|abstain]\ngov-cli vote drep <gov_action> [yes|no|abstain]\n"})}),"\n",(0,n.jsx)(o.h3,{id:"examples",children:"examples:"}),"\n",(0,n.jsx)(o.pre,{children:(0,n.jsx)(o.code,{className:"language-bash",children:"gov-cli vote drep ea478d10558aa77247440cfbf053bfd5d219003fcde26bd1e3204d738711d076#0         # vote yes\ngov-cli vote drep ea478d10558aa77247440cfbf053bfd5d219003fcde26bd1e3204d738711d076#0 yes     # vote yes\ngov-cli vote drep ea478d10558aa77247440cfbf053bfd5d219003fcde26bd1e3204d738711d076#0 no      # vote no\ngov-cli vote drep ea478d10558aa77247440cfbf053bfd5d219003fcde26bd1e3204d738711d076#0 abstain # vote abstain\n"})}),"\n",(0,n.jsx)(o.h3,{id:"cast-vote-with-cc-keys",children:"Cast vote with cc keys"}),"\n",(0,n.jsx)(o.pre,{children:(0,n.jsx)(o.code,{children:"gov-cli cc vote <gov_action> [yes|no|abstain]\ngov-cli vote cc <gov_action> [yes|no|abstain]\n"})})]})}function v(e={}){const{wrapper:o}={...(0,s.R)(),...e.components};return o?(0,n.jsx)(o,{...e,children:(0,n.jsx)(l,{...e})}):l(e)}},8453:(e,o,t)=>{t.d(o,{R:()=>i,x:()=>d});var n=t(6540);const s={},c=n.createContext(s);function i(e){const o=n.useContext(c);return n.useMemo((function(){return"function"==typeof e?e(o):{...o,...e}}),[o,e])}function d(e){let o;return o=e.disableParentContext?"function"==typeof e.components?e.components(s):e.components||s:i(e.components),n.createElement(c.Provider,{value:o},e.children)}}}]);