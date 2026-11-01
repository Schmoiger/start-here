#!/usr/bin/env node
"use strict";
// Optional ts-morph extraction helper for spec_indexer.py (T-015).
// Invoked as:  node ts_extract.mjs <abs-file>
// The indexer skips this backend quietly when node or ts-morph is unavailable.
// ts-morph is resolved from the repository root (cwd) so workspace installs work.

const { createRequire } = require("module");
const requireFromRepo = createRequire(process.cwd() + "/noop.js");

let Project;
let SyntaxKind;
try {
  ({ Project, SyntaxKind } = requireFromRepo("ts-morph"));
} catch (err) {
  process.exit(0); // not available — signal "nothing produced"; indexer degrades quietly
}

const filePath = process.argv[2];
if (!filePath) {
  console.error("usage: node ts_extract.mjs <abs-file>");
  process.exit(1);
}

const project = new Project({
  skipAddingFilesFromTsConfig: true,
  skipFileDependencyResolution: true,
});
const sf = project.addSourceFileAtPath(filePath);

const symbols = [];
const imports = [];
const usages = [];

function push(kind, name, signature, line, decorators, props) {
  symbols.push({
    kind,
    name,
    signature,
    line,
    decorators: decorators || [],
    props: props || [],
  });
}

for (const fn of sf.getFunctions()) {
  const params = fn.getParameters().map((p) => p.getText()).join(", ");
  push(
    "function",
    fn.getName() || "",
    `(${params})`,
    fn.getStartLineNumber(),
    fn.getDecorators().map((d) => d.getText()),
    params,
  );
}

for (const cls of sf.getClasses()) {
  push(
    "class",
    cls.getName() || "",
    "",
    cls.getStartLineNumber(),
    cls.getDecorators().map((d) => d.getText()),
    [],
  );
  for (const m of cls.getMethods()) {
    const params = m.getParameters().map((p) => p.getText()).join(", ");
    push(
      "method",
      `${cls.getName() || ""}.${m.getName()}`,
      `(${params})`,
      m.getStartLineNumber(),
      m.getDecorators().map((d) => d.getText()),
      [],
    );
  }
}

for (const itf of sf.getInterfaces()) {
  push("interface", itf.getName() || "", "", itf.getStartLineNumber(), [], []);
}
for (const ta of sf.getTypeAliases()) {
  push("type", ta.getName() || "", "", ta.getStartLineNumber(), [], []);
}

for (const vs of sf.getVariableStatements()) {
  for (const decl of vs.getDeclarations()) {
    const init = decl.getInitializer();
    const name = decl.getName();
    const line = decl.getStartLineNumber();
    if (init && init.getKind() === SyntaxKind.ArrowFunction) {
      const params = init.getParameters().map((p) => p.getText()).join(", ");
      push("const_arrow", name, `(${params})`, line, [], params);
    } else {
      push("const", name, "", line, [], []);
    }
  }
}

for (const imp of sf.getImportDeclarations()) {
  const modulePath = imp.getModuleSpecifierValue();
  if (modulePath) {
    imports.push(modulePath);
  }
}

for (const el of sf.getDescendantsOfKind(SyntaxKind.JsxOpeningElement)) {
  const node = el.getTagNameNode ? el.getTagNameNode() : null;
  if (node) {
    usages.push(node.getText().split(".").pop());
  }
}
for (const el of sf.getDescendantsOfKind(SyntaxKind.JsxSelfClosingElement)) {
  const node = el.getTagNameNode ? el.getTagNameNode() : null;
  if (node) {
    usages.push(node.getText().split(".").pop());
  }
}

process.stdout.write(JSON.stringify({ symbols, imports, usages }));
