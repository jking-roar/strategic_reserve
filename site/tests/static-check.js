import { access, readFile } from "node:fs/promises";
const html=await readFile(new URL("../index.html",import.meta.url),"utf8");
for(const match of html.matchAll(/(?:src|href)="(\.\/[^"]+)"/g)) await access(new URL(`../${match[1].slice(2)}`,import.meta.url));
if(/(?:src|href)="\//.test(html)) throw new Error("Domain-root asset reference found");
console.log("Static assets and subpath-safe references verified.");
