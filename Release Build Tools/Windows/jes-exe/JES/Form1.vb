Public Class Form1

    Public Sub New()

        ' This call is required by the Windows Form Designer.
        InitializeComponent()

        ' Add any initialization after the InitializeComponent() call.
        Me.Show()
        Shell("jes.bat", AppWinStyle.Hide, False)
        System.Threading.Thread.Sleep(5000)

        End
    End Sub
End Class
