//
//  InformationContainerView.swift
//  PicTeX
//
//  Created by Erica Chiang on 8/23/20.
//  Copyright © 2020 Erica Chiang. All rights reserved.
//

import SwiftUI

struct InformationContainerView: View {
    var body: some View {
        VStack(alignment: .leading) {
            InformationDetailView(title: "Step 1", subTitle: "Take a picture of your writeup", imageName: "camera")

            InformationDetailView(title: "Step 2", subTitle: "Review your .tex file and confirm that it looks correct.", imageName: "checkmark.circle")

            InformationDetailView(title: "Step 3", subTitle: "Download your new .tex file!", imageName: "arrow.down.doc")
        }
        .padding(.horizontal)
    }
}

struct InformationContainerView_Previews: PreviewProvider {
    static var previews: some View {
        InformationContainerView()
    }
}
