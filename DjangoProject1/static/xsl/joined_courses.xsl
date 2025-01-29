<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/courses">
        <html lang="pl">
            <head>
                <title>Courses_xml</title>
                <meta charset="UTF-8" />
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        color: #333;
                        margin: 0;
                        padding: 20px;
                    }
                    h1 {
                        text-align: center;
                        color: #2c3e50;
                    }
                    table {
                        width: 80%;
                        margin: 20px auto;
                        border-collapse: collapse;
                        background-color: #fff;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 10px;
                        text-align: left;
                    }
                    th {
                        background-color: #0d26e6;
                        color: white;
                        text-transform: uppercase;
                    }
                    tr:nth-child(even) {
                        background-color: #f9f9f9;
                    }
                    tr:hover {
                        background-color: #f1f1f1;
                    }
                    td {
                        font-size: 14px;
                    }
                </style>
            </head>
            <body>
                <h1>Joined Courses</h1>
                <table border="1">
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Teacher</th>
                        <th>Created</th>
                    </tr>
                    <xsl:for-each select="course">
                        <tr>
                            <td><xsl:value-of select="name" /></td>
                            <td><xsl:value-of select="description" /></td>
                            <td><xsl:value-of select="teacher" /></td>
                            <td>
                                <xsl:value-of select="substring(created, 1, 10)" />
                                <xsl:text> </xsl:text>
                                <xsl:value-of select="substring(created, 12, 5)" />
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
