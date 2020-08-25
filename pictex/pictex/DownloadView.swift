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
        Button("Cick here to download") {UIApplication.shared.open(URL(string: self.cflink + self.key)!)}
            .padding()
            .frame(maxWidth: .infinity)
            .padding()
            .foregroundColor(.green)
        //Spacer()
        
    }
}

struct DownloadView_Previews: PreviewProvider {
    static var previews: some View {
        DownloadView(key: .constant(""))
    }
}
