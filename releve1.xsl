<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8"/>
    <xsl:template match="/">
        <html>
            <head>
                <title>Relevé bancaire</title>
            </head>
            <body>
                <h1>Relevé bancaire</h1>
                <ul>
                    <li>RIB : <xsl:value-of select="releve/@RIB"/></li>
                    <li>Date du relevé : <xsl:value-of select="releve/dateReleve"/></li>
                    <li>Solde : <xsl:value-of select="releve/solde"/></li>
                    <li>Période : du <xsl:value-of select="releve/operations/@dateDebut"/>
                        au <xsl:value-of select="releve/operations/@dateFin"/></li>
                </ul>
                <table border="1" width="90%">
                    <tr>
                        <th>Type</th><th>Date</th><th>Montant</th><th>Description</th>
                    </tr>
                    <xsl:for-each select="releve/operations/operation">
                        <tr>
                            <td><xsl:value-of select="@type"/></td>
                            <td><xsl:value-of select="@date"/></td>
                            <td><xsl:value-of select="@montant"/></td>
                            <td><xsl:value-of select="@description"/></td>
                        </tr>
                    </xsl:for-each>
                    <tr>
                        <td colspan="3">Total des opérations de débit</td>
                        <td><xsl:value-of select="sum(releve/operations/operation[@type='DEBIT']/@montant)"/></td>
                    </tr>
                    <tr>
                        <td colspan="3">Total des opérations de crédit</td>
                        <td><xsl:value-of select="sum(releve/operations/operation[@type='CREDIT']/@montant)"/></td>
                    </tr>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
