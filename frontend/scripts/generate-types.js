#!/usr/bin/env node
import { writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import openapiTS from "openapi-typescript";

const currentDir = dirname(fileURLToPath(import.meta.url));
const schemaPath = resolve(currentDir, "../schema/openapi.json");
const outputPath = resolve(currentDir, "../src/lib/types/backend.d.ts");

const types = await openapiTS(schemaPath, {
  transform: (schemaObject, { path }) => {
    if (path.includes("/auth")) {
      schemaObject.description = `${schemaObject.description ?? ""} (auth)`;
    }
    return schemaObject;
  }
});

await writeFile(outputPath, "// Generated via frontend/scripts/generate-types.js\n" + types, "utf8");
console.log(`Types generated at ${outputPath}`);
