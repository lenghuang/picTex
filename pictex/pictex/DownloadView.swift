//
//  DownloadView.swift
//  pictex
//
//  Created by Erica Chiang on 8/24/20.
//  Copyright © 2020 PicTex Technologies. All rights reserved.
//

import SwiftUI

struct DownloadView: View {
    @Binding var key: String
    var cflink = "https://d37crjhbub9zgu.cloudfront.net/"
    var body: some View {
        VStack {
            Spacer()
            Text("Conversion Complete!")
                .font(.largeTitle)
                .fontWeight(.semibold)
            Image(systemName: "checkmark.circle").resizable().foregroundColor(Color.green).frame(width: 300.0, height: 300.0)
            Spacer()
            Text("Click here to get a download link to your TeX file:")
            Button("Download TeX File") {UIApplication.shared.open(URL(string: self.cflink + self.key)!)}
                .padding()
                .frame(maxWidth: .infinity)
                .padding()
                .foregroundColor(.green)
            Spacer()
        }
    }
}

struct DownloadView_Previews: PreviewProvider {
    static var previews: some View {
        DownloadView(key: .constant(""))
    }
}
