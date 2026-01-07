# 📋 GUIA SSOT — Single Source of Truth

> **Regra de Ouro:** Cada informação tem UM lugar onde é definida. Outros arquivos APONTAM, não copiam.

---

## 🏛️ ONDE DEFINIR CADA COISA

| Informação | Arquivo SSOT | O que NÃO fazer |
| :--- | :--- | :--- |
| **Hierarquia, Patronos, Protocolo** | `01_MAGNA_CARTA.md` | Não redefinir hierarquia em outro lugar |
| **GUARDIÕES** (cores, virtudes, evolução) | `02_LIVRO_DO_REINO.md` | ⚠️ Nunca recopiar tabela de Guardiões |
| **Tempos, durações, fases por idade** | `03_MATRIZ_EVOLUCAO.md` | Não colocar tempos em lições |
| **Rituais, ferramentas, liturgia** | `04_MANUAL_OFICIO.md` | OK repetir instruções de ritual |
| **Mesas, Especialistas, Verificação** | `05_SISTEMA_EXCELENCIA.md` | Workflows apontam, não redefinem |

---

## 🔗 COMO APONTAR (Boas Práticas)

### ❌ ERRADO (Duplicar)
```markdown
## Guardiões
| Nome | Cor | Virtude |
| Melquior | #D4A84B | Sabedoria |
...
```

### ✅ CERTO (Apontar)
```markdown
> Para detalhes dos Guardiões, consulte [02_LIVRO_DO_REINO](link).
```

---

## 📂 ESTRUTURA DE PASTAS

```
GOVERNANCA/
├── 00-05 (Canônicos)   ← SSOT, editar com cuidado
├── 99_TEMPORARIO.md    ← Rascunho do momento
├── _LOGS/              ← Histórico (não editar após salvar)
├── _ARCHIVE/           ← Mortos (não consultar)
└── _LEGADO/            ← Referência (pode virar _ARCHIVE)
```

---

## ⚠️ REGRAS PARA O ARQUITETO IA

1. **Antes de definir algo:** Verificar se já existe em 01-05
2. **Se existe:** APONTAR com link, não copiar
3. **Discussões do dia:** Salvar em `_LOGS/` ao final
4. **99_TEMPORARIO:** Limpar após consolidar

---

*Atualizado: 2026-01-07*
