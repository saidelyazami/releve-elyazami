"""Activité pratique Technologie XML : relevé bancaire.

Application Streamlit qui valide les documents XML (DTD et XSD)
et affiche le résultat des feuilles de style XSL.
"""
import io
from pathlib import Path

import streamlit as st
from lxml import etree

BASE = Path(__file__).parent

st.set_page_config(page_title="Relevé bancaire XML", page_icon="🏦", layout="wide")


def lire(nom: str) -> str:
    return (BASE / nom).read_text(encoding="utf-8")


def parser_xml(texte: str):
    """Parse un XML sans charger de ressource externe."""
    parser = etree.XMLParser(load_dtd=False, no_network=True, resolve_entities=False)
    return etree.fromstring(texte.encode("utf-8"), parser)


def valider_dtd(xml_texte: str, dtd_texte: str):
    # On retire la déclaration <?xml ...?> de la DTD externe avant de la charger
    lignes = [l for l in dtd_texte.splitlines() if not l.strip().startswith("<?xml")]
    dtd = etree.DTD(io.StringIO("\n".join(lignes)))
    doc = parser_xml(xml_texte)
    return dtd.validate(doc), [str(e) for e in dtd.error_log]


def valider_xsd(xml_texte: str, xsd_texte: str):
    schema = etree.XMLSchema(parser_xml(xsd_texte))
    doc = parser_xml(xml_texte)
    return schema.validate(doc), [str(e) for e in schema.error_log]


def transformer(xml_texte: str, xsl_texte: str) -> str:
    xslt = etree.XSLT(parser_xml(xsl_texte))
    return str(xslt(etree.ElementTree(parser_xml(xml_texte))))


def afficher_validation(ok: bool, erreurs: list[str]):
    if ok:
        st.success("Document valide ✅")
    else:
        st.error("Document non valide ❌")
        for e in erreurs:
            st.code(e)


st.title("🏦 Relevé bancaire — Technologie XML")
st.caption("Activité pratique : DTD, schéma XML (XSD) et feuilles de style XSL")

onglets = st.tabs([
    "1. Arbre XML",
    "2. DTD",
    "3. Schéma XSD",
    "4. XSL : tout le relevé",
    "5. XSL : opérations CREDIT",
])

# 1. Arbre XML
with onglets[0]:
    st.subheader("Structure de l'arbre XML")
    st.code(
        """releve  (@RIB)
├── dateReleve      → texte
├── solde           → texte
└── operations  (@dateDebut, @dateFin)
    └── operation +  (@type, @date, @montant, @description)""",
        language="text",
    )

# 2. DTD
with onglets[1]:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**releve.dtd**")
        dtd_texte = st.text_area("DTD", lire("releve.dtd"), height=420, key="dtd")
    with col2:
        st.markdown("**releve.xml**")
        xml_dtd = st.text_area("XML", lire("releve.xml"), height=420, key="xml_dtd")
    try:
        afficher_validation(*valider_dtd(xml_dtd, dtd_texte))
    except etree.XMLSyntaxError as e:
        st.error(f"Erreur de syntaxe : {e}")
    except etree.DTDParseError as e:
        st.error(f"Erreur dans la DTD : {e}")

# 3. XSD
with onglets[2]:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**releve.xsd**")
        xsd_texte = st.text_area("XSD", lire("releve.xsd"), height=420, key="xsd")
    with col2:
        st.markdown("**releve_xsd.xml**")
        xml_xsd = st.text_area("XML", lire("releve_xsd.xml"), height=420, key="xml_xsd")
    try:
        afficher_validation(*valider_xsd(xml_xsd, xsd_texte))
    except (etree.XMLSyntaxError, etree.XMLSchemaParseError) as e:
        st.error(f"Erreur : {e}")


def onglet_xsl(xml_nom: str, xsl_nom: str, cle: str):
    with st.expander(f"Voir / modifier le code ({xml_nom}, {xsl_nom})"):
        col1, col2 = st.columns(2)
        with col1:
            xml_texte = st.text_area(xml_nom, lire(xml_nom), height=380, key=f"xml_{cle}")
        with col2:
            xsl_texte = st.text_area(xsl_nom, lire(xsl_nom), height=380, key=f"xsl_{cle}")
    try:
        html = transformer(xml_texte, xsl_texte)
        mode = st.segmented_control(
            "Affichage",
            ["Rendu", "Code HTML", "Les deux"],
            default="Rendu",
            key=f"mode_{cle}",
        ) or "Rendu"
        if mode == "Rendu":
            with st.container(border=True):
                st.html(html)
        elif mode == "Code HTML":
            st.code(html, language="html")
        else:
            col_rendu, col_code = st.columns(2)
            with col_rendu:
                st.markdown("**Rendu**")
                with st.container(border=True):
                    st.html(html)
            with col_code:
                st.markdown("**Code HTML**")
                st.code(html, language="html")
        st.download_button("Télécharger le HTML", html, file_name=xsl_nom.replace(".xsl", ".html"),
                           mime="text/html", key=f"dl_{cle}")
    except (etree.XMLSyntaxError, etree.XSLTParseError, etree.XSLTApplyError) as e:
        st.error(f"Erreur : {e}")


# 4. XSL tout le relevé
with onglets[3]:
    st.subheader("Toutes les données + totaux débit / crédit")
    onglet_xsl("releve.xml", "releve1.xsl", "q4")

# 5. XSL CREDIT
with onglets[4]:
    st.subheader("Opérations de type CREDIT")
    onglet_xsl("releve_xsd.xml", "releve2.xsl", "q5")
