# releve-elyazami

Activité pratique Technologie XML : gestion de relevés de comptes bancaires.

| Fichier | Rôle |
|---|---|
| `releve.dtd` | DTD décrivant la structure du relevé |
| `releve.xml` | Relevé valide par rapport à la DTD (affiché avec `releve1.xsl`) |
| `releve.xsd` | Schéma XML du relevé |
| `releve_xsd.xml` | Relevé valide par rapport au schéma (affiché avec `releve2.xsl`) |
| `releve1.xsl` | Affiche toutes les données + total des débits et des crédits |
| `releve2.xsl` | Affiche uniquement les opérations de type CREDIT |

## Arbre XML

```
releve  (@RIB)
├── dateReleve
├── solde
└── operations  (@dateDebut, @dateFin)
    └── operation +  (@type, @date, @montant, @description)
```
<img width="1730" height="417" alt="image" src="https://github.com/user-attachments/assets/de1f7be0-43e7-4d7e-a1d7-dfe2b75b6b50" />

<img width="1745" height="243" alt="image" src="https://github.com/user-attachments/assets/47ea227b-1d6a-4c76-a929-d511422e587b" />

