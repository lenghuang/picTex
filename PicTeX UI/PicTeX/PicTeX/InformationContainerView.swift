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
            InformationDetailView(title: "Step 1", subTitle: "Take a picture of your writeup", imageName: "slider.horizontal.below.rectangle")

            InformationDetailView(title: "Step 2", subTitle: "Review your .tex file and confirm that it looks correct.", imageName: "minus.slash.plus")

            InformationDetailView(title: "Step 3", subTitle: "Download your new .tex file!", imageName: "checkmark.square")
        }
        .padding(.horizontal)
    }
}

struct InformationContainerView_Previews: PreviewProvider {
    static var previews: some View {
        InformationContainerView()
    }
}
