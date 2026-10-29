import test from 'node:test';
import assert from 'node:assert/strict';
import { energyKWh, energyCost, ratedYieldMonths, costPerPage } from './calculations.mjs';
test('energy units and entered tariff',()=>{
  assert.equal(energyKWh(1000,2),2);
  assert.equal(energyCost(1000,2,0.30),0.60);
  assert.equal(energyKWh(0,24),0);
  assert.equal(energyCost(200,0,0.4),0);
});
test('workload scenarios and unit price',()=>{
  assert.equal(ratedYieldMonths(3000,300),10);
  assert.equal(costPerPage(60,3000),0.02);
  assert.equal(costPerPage(0,3000),0);
});
test('invalid inputs cannot silently produce a result',()=>{
  for(const n of [-1,NaN,Infinity,'100',null]) assert.throws(()=>energyKWh(n,2),RangeError);
  assert.throws(()=>ratedYieldMonths(3000,0),RangeError);
  assert.throws(()=>costPerPage(60,0),RangeError);
  assert.throws(()=>energyCost(1000,2,-0.1),RangeError);
});
