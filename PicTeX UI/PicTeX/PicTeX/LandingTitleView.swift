//
//  LandingTitleView.swift
//  PicTeX
//
//  Created by Erica Chiang on 8/23/20.
//  Copyright © 2020 Erica Chiang. All rights reserved.
//

import SwiftUI

struct LandingTitleView: View {
    var body: some View {
        VStack {
            Image("gradientsIcon")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(width: 180, alignment: .center)
                .accessibility(hidden: true)

            Text("Welcome to")
                .fontWeight(.black)
                .font(.system(size: 36))

            Text("PicTeX")
                .fontWeight(.black)
                .font(.system(size: 36))
                .foregroundColor(.green)
        }
    }
}

struct LandingTitleView_Previews: PreviewProvider {
    static var previews: some View {
        LandingTitleView()
    }
}
