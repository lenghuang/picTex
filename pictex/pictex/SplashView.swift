//
//  SplashView.swift
//  PicTeX
//
//  Created by Erica Chiang on 8/23/20.
//  Copyright © 2020 Erica Chiang. All rights reserved.
//
// Structure from https://mobiraft.com/ios/swiftui/how-to-add-splash-screen-in-swiftui/

import SwiftUI

struct SplashView: View {
    @State var isActive:Bool = false
    
    var body: some View {
        VStack {
            if self.isActive {
                LandingView()
            } else {
                VStack {
                    CircleImage()
                    
                    Text("PicTeX")
                        .font(Font.largeTitle)
                        .foregroundColor(Color.red)
                }
                
            }
        }
            
        .onAppear {
            DispatchQueue.main.asyncAfter(deadline: .now() + 2.5) {
                withAnimation {
                    self.isActive = true
                }
            }
        }
    }
    
}

struct SplashView_Previews: PreviewProvider {
    static var previews: some View {
        SplashView()
    }
}
