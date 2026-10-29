window.addEventListener('load',()=>document.querySelector('.loader')?.classList.add('hide'));
const menu=document.querySelector('.menu'),nav=document.querySelector('nav');if(menu)menu.onclick=()=>nav.classList.toggle('open');
const obs=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('show');obs.unobserve(e.target)}}),{threshold:.08});document.querySelectorAll('.reveal').forEach(e=>obs.observe(e));
