(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[679],{2028:function(e,n,t){(window.__NEXT_P=window.__NEXT_P||[]).push(["/hi",function(){return t(2022)}])},2022:function(e,n,t){"use strict";t.r(n),t.d(n,{default:function(){return g}});var r=t(7568),o=t(1799),a=t(9396),s=t(797),u=t(655),i=t(5893),c=t(7294),f=t(1163),l=t(4597),p=(t(5202),t(949)),v=t(3236),h=t(9008),x=t.n(h);function g(){var e=(0,c.useState)({is_hydrated:!1,events:[{name:"state.hydrate"}],files:[]}),n=e[0],t=e[1],h=(0,c.useState)({state:null,events:[],processing:!1}),g=h[0],d=h[1],_=(0,f.useRouter)(),m=(0,c.useRef)(null),w=_.isReady,y=(0,p.If)();y.colorMode,y.toggleColorMode;return(0,c.useEffect)((function(){if(w){m.current||(0,l.$j)(m,n,t,g,d,_,"ws://localhost:8000/event",["websocket","polling"]);var e=function(){var e=(0,r.Z)((function(){return(0,u.__generator)(this,(function(e){switch(e.label){case 0:return null!=g.state&&(t((0,a.Z)((0,o.Z)({},g.state),{events:(0,s.Z)(n.events).concat((0,s.Z)(g.events))})),d({state:null,events:[],processing:!1})),[4,(0,l.xq)(n,t,g,d,_,m.current)];case 1:return e.sent(),[2]}}))}));return function(){return e.apply(this,arguments)}}();e()}})),(0,i.jsxs)(v.X6,{children:["HI",(0,i.jsxs)(x(),{children:[(0,i.jsx)("title",{children:"Pynecone App"}),(0,i.jsx)("meta",{content:"A Pynecone app.",name:"description"}),(0,i.jsx)("meta",{content:"favicon.ico",property:"og:image"})]})]})}},4597:function(e,n,t){"use strict";t.d(n,{$j:function(){return _},xq:function(){return d}});var r,o=t(7568),a=t(1799),s=t(9396),u=t(655),i=t(9669),c=t.n(i),f=t(9367),l=t(1142),p=t.n(l),v="token",h=function(){return r||(window&&(window.sessionStorage.getItem(v)||window.sessionStorage.setItem(v,function(){var e=(new Date).getTime(),n=performance&&performance.now&&1e3*performance.now()||0;return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,(function(t){var r=16*Math.random();return e>0?(r=(e+r)%16|0,e=Math.floor(e/16)):(r=(n+r)%16|0,n=Math.floor(n/16)),("x"==t?r:7&r|8).toString(16)}))}()),r=window.sessionStorage.getItem(v)),r)},x=function(e,n){for(var t in n){for(var r=e,o=t.split(".").slice(1);o.length>0;)r=r[o.shift()];for(var a in n[t])r[a]=n[t][a]}},g=function(){var e=(0,o.Z)((function(e,n,t){return(0,u.__generator)(this,(function(r){return"_redirect"==e.name?(n.push(e.payload.path),[2,!1]):"_console"==e.name?(console.log(e.payload.message),[2,!1]):"_alert"==e.name?(alert(e.payload.message),[2,!1]):"_set_value"==e.name?(e.payload.ref.current.value=e.payload.value,[2,!1]):(e.token=h(),e.router_data={pathname:(o=n).pathname,query:o.query},t?(t.emit("event",JSON.stringify(e)),[2,!0]):[2,!1]);var o}))}));return function(n,t,r){return e.apply(this,arguments)}}(),d=function(){var e=(0,o.Z)((function(e,n,t,r,o,i){var c;return(0,u.__generator)(this,(function(u){switch(u.label){case 0:return t.processing||0==e.events.length?[2]:(r((0,s.Z)((0,a.Z)({},t),{processing:!0})),c=e.events.shift(),n((0,s.Z)((0,a.Z)({},e),{events:e.events})),[4,g(c,o,i)]);case 1:return u.sent()||r((0,s.Z)((0,a.Z)({},e),{processing:!1})),[2]}}))}));return function(n,t,r,o,a,s){return e.apply(this,arguments)}}(),_=function(){var e=(0,o.Z)((function(e,n,t,r,o,a,s,i){var c;return(0,u.__generator)(this,(function(u){return c=new URL(s),e.current=(0,f.ZP)(s,{path:c.pathname,transports:i,autoUnref:!1}),e.current.on("connect",(function(){d(n,t,r,o,a,e.current)})),e.current.on("event",(function(e){e=p().parse(e),x(n,e.delta),o({processing:!0,state:n,events:e.events})})),[2]}))}));return function(n,t,r,o,a,s,u,i){return e.apply(this,arguments)}}();!function(){var e=(0,o.Z)((function(e,n,t,r,o,i){var f,l,p;return(0,u.__generator)(this,(function(u){switch(u.label){case 0:if(n.processing||0==r.length)return[2];for(t((0,s.Z)((0,a.Z)({},n),{processing:!0})),f={"Content-Type":r[0].type},l=new FormData,p=0;p<r.length;p++)l.append("files",r[p],h()+":"+o+":"+r[p].name);return[4,c().post(i,l,f).then((function(n){var r=n.data;x(e,r.delta),t({processing:!1,state:e,events:r.events})}))];case 1:return u.sent(),[2]}}))}))}()}},function(e){e.O(0,[760,774,888,179],(function(){return n=2028,e(e.s=n);var n}));var n=e.O();_N_E=n}]);