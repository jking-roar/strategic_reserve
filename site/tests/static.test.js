import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
const html=await readFile(new URL("../index.html",import.meta.url),"utf8"),css=await readFile(new URL("../styles.css",import.meta.url),"utf8");
test("page uses only relative local runtime assets",()=>{for(const match of html.matchAll(/<(?:script|link)[^>]+(?:src|href)="([^"]+)"/g)){const value=match[1];assert.ok(value.startsWith("./"),`${value} must be a subpath-safe local asset`);}});
test("semantic shell remains meaningful without enhancements",()=>{for(const text of ["Strategic Reserve","HTML edition","Mark Steere","Start a game","Project repository"])assert.match(html,new RegExp(text,"i"));assert.match(html,/role="grid"/);assert.match(html,/role="status"/);assert.match(html,/aria-live="polite"/);assert.match(html,/<dialog/);});
test("keyboard and non-color-only visual contracts are present",()=>{assert.match(css,/:focus-visible/);assert.match(css,/\.cell\.legal::after/);assert.match(css,/\.cell\.target::before/);assert.match(css,/prefers-reduced-motion/);});
test("board uses six equal shrinkable tracks in both dimensions",()=>{const boardRule=css.match(/\.board\s*\{([^}]*)\}/)?.[1]??"";assert.match(boardRule,/grid-template-columns:\s*repeat\(6,\s*minmax\(0,\s*1fr\)\)/);assert.match(boardRule,/grid-template-rows:\s*repeat\(6,\s*minmax\(0,\s*1fr\)\)/);});
test("controller source preserves required interaction contracts",async()=>{const app=await readFile(new URL("../js/app.js",import.meta.url),"utf8");assert.match(app,/generation!==session/g);assert.match(app,/cancelAI\(\).*dialog\.showModal/s);assert.match(app,/rollButton\.focus\(\)/);assert.match(app,/dialog\.addEventListener\("cancel"/);assert.match(app,/input\[name="mode"\]/);});
