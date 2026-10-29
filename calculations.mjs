/** Planning math only. Inputs are user-supplied; no OEM compatibility/merchant data. */
function nonnegative(n,name){if(typeof n!=='number'||!Number.isFinite(n)||n<0)throw new RangeError(name+' must be a finite nonnegative number');return n;}
function positive(n,name){nonnegative(n,name);if(n===0)throw new RangeError(name+' must be greater than zero');return n;}
export function energyKWh(watts,hours){return nonnegative(watts,'watts')*nonnegative(hours,'hours')/1000;}
export function energyCost(watts,hours,costPerKWh){return energyKWh(watts,hours)*nonnegative(costPerKWh,'costPerKWh');}
export function ratedYieldMonths(yieldPages,pagesPerMonth){return positive(yieldPages,'yieldPages')/positive(pagesPerMonth,'pagesPerMonth');}
export function costPerPage(cartridgeCost,yieldPages){return nonnegative(cartridgeCost,'cartridgeCost')/positive(yieldPages,'yieldPages');}
