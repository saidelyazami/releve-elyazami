<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8"/>
    <xsl:template match="/">
        <html>
            <head>
                <title>Opérations de crédit</title>
            </head>
            <body>
                <h1>Opérations de type CREDIT</h1>
                <p>RIB : <xsl:value-of select="releve/@RIB"/></p>
                <table border="1" width="90%">
                    <tr>
                        <th>Date</th><th>Montant</th><th>Description</th>
                    </tr>
                    <xsl:for-each select="releve/operations/operation[@type='CREDIT']">
                        <tr>
                            <td><xsl:value-of select="@date"/></td>
                            <td><xsl:value-of select="@montant"/></td>
                            <td><xsl:value-of select="@description"/></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
