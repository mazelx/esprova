window.Modernizr=function(e,n,t){function o(e){p.cssText=e}function r(e,n){return o(v.join(e+";")+(n||""))}function i(e,n){return typeof e===n}function u(e,n){return!!~(""+e).indexOf(n)}function c(e,n,o){for(var r in e){var u=n[e[r]];if(u!==t)return o===!1?e[r]:i(u,"function")?u.bind(o||n):u}return!1}var a="2.8.3",s={},f=n.documentElement,l="modernizr",d=n.createElement(l),p=d.style,y,m={}.toString,v=" -webkit- -moz- -o- -ms- ".split(" "),h={},b={},w={},C=[],T=C.slice,j,E=function(e,t,o,r){var i,u,c,a,s=n.createElement("div"),d=n.body,p=d||n.createElement("body");if(parseInt(o,10))for(;o--;)c=n.createElement("div"),c.id=r?r[o]:l+(o+1),s.appendChild(c);return i=["&#173;",'<style id="s',l,'">',e,"</style>"].join(""),s.id=l,(d?s:p).innerHTML+=i,p.appendChild(s),d||(p.style.background="",p.style.overflow="hidden",a=f.style.overflow,f.style.overflow="hidden",f.appendChild(p)),u=t(s,e),d?s.parentNode.removeChild(s):(p.parentNode.removeChild(p),f.style.overflow=a),!!u},g={}.hasOwnProperty,x;x=i(g,"undefined")||i(g.call,"undefined")?function(e,n){return n in e&&i(e.constructor.prototype[n],"undefined")}:function(e,n){return g.call(e,n)},Function.prototype.bind||(Function.prototype.bind=function(e){var n=this;if("function"!=typeof n)throw new TypeError;var t=T.call(arguments,1),o=function(){if(this instanceof o){var r=function(){};r.prototype=n.prototype;var i=new r,u=n.apply(i,t.concat(T.call(arguments)));return Object(u)===u?u:i}return n.apply(e,t.concat(T.call(arguments)))};return o}),h.touch=function(){var t;return"ontouchstart"in e||e.DocumentTouch&&n instanceof DocumentTouch?t=!0:E(["@media (",v.join("touch-enabled),("),l,")","{#modernizr{top:9px;position:absolute}}"].join(""),function(e){t=9===e.offsetTop}),t};for(var z in h)x(h,z)&&(j=z.toLowerCase(),s[j]=h[z](),C.push((s[j]?"":"no-")+j));return s.addTest=function(e,n){if("object"==typeof e)for(var o in e)x(e,o)&&s.addTest(o,e[o]);else{if(e=e.toLowerCase(),s[e]!==t)return s;n="function"==typeof n?n():n,"undefined"!=typeof enableClasses&&enableClasses&&(f.className+=" "+(n?"":"no-")+e),s[e]=n}return s},o(""),d=y=null,s._version=a,s._prefixes=v,s.testStyles=E,s}(this,this.document);