//
//  LandingView.swift
//  pictex
//
//  Created by Len Huang on 8/21/20.
//  Copyright © 2020 PicTex Technologies. All rights reserved.
//

import SwiftUI

struct LandingView: View {
    var body: some View {
        VStack{
            Spacer()
            Text("PicTex")
                .font(.largeTitle)
                .fontWeight(.heavy)
                .multilineTextAlignment(.center)
            Text("Converting your math homework to LaTeX files and pdfs!")
                .font(.subheadline)
                .multilineTextAlignment(.center)
                .padding(.top, 5.0)
            Spacer()
            Image("process").resizable()
                .aspectRatio(contentMode : .fit)
                .padding(.all, 10.0)
            Spacer()
            Text("Get Started Button")
            Spacer()
        }
    }
}

struct LandingView_Previews: PreviewProvider {
    static var previews: some View {
        LandingView()
    }
}
