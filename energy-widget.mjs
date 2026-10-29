import {energyKWh,energyCost} from './calculations.mjs';
class VyonetixEnergy extends HTMLElement{
  connectedCallback(){
    if(this.shadowRoot)return;
    const root=this.attachShadow({mode:'open'});
    root.innerHTML=`<style>:host{display:block;font:16px/1.5 system-ui;color:#142942}section{padding:24px;background:linear-gradient(120deg,#fffdf6,#fef3c7);border:1px solid #e1bd64;border-top:5px solid #f59e0b;border-radius:14px}label{display:block;margin:12px 0}input,button{font:inherit;padding:8px;border-radius:6px}input{width:110px;border:1px solid #668}button{background:#075f66;color:white;border:0;cursor:pointer}a{color:#075f66}</style><section><h2>Electricity use scenario</h2><p>Use measured power and your own tariff. A result is an estimate.</p><form><label>Power (W) <input name="watts" type="number" min="0" step="any" value="100" required></label><label>Operating hours <input name="hours" type="number" min="0" step="any" value="8" required></label><label>Cost per kWh <input name="tariff" type="number" min="0" step="any" value="0.30" required></label><button>Calculate</button></form><p role="status" aria-live="polite"></p><a href="https://deals.vyonetixsolutions.com.au/tools/electricity-cost/?utm_source=developer_widget&amp;utm_medium=referral&amp;utm_campaign=energy-kit" target="_blank" rel="noopener">Open the Vyonetix electricity tool</a></section>`;
    const form=root.querySelector('form'),status=root.querySelector('[role=status]');
    const calculate=()=>{try{const d=new FormData(form),w=Number(d.get('watts')),h=Number(d.get('hours')),t=Number(d.get('tariff'));status.textContent=`Estimated energy: ${energyKWh(w,h).toFixed(3)} kWh. Estimated cost: ${energyCost(w,h,t).toFixed(2)} in the currency of your tariff.`;}catch(e){status.textContent=e.message;}};
    form.addEventListener('submit',e=>{e.preventDefault();if(form.reportValidity())calculate();});calculate();
  }
}
if(!customElements.get('vyonetix-energy'))customElements.define('vyonetix-energy',VyonetixEnergy);
