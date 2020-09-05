//
//  LandingView.swift
//  PicTeX
//
//  Created by Erica Chiang on 8/23/20.
//  Copyright © 2020 Erica Chiang. All rights reserved.
//

import SwiftUI

struct LandingView: View {
    var body: some View {
        NavigationView {
            
            VStack(alignment: .center) {
                
                LandingTitleView()
                    .navigationBarTitle("")
                    .navigationBarHidden(true)
                
                InformationContainerView()
                
                Spacer(minLength: 30)
                
                Button(action: {
                    let generator = UINotificationFeedbackGenerator()
                    generator.notificationOccurred(.success)
                }) {
                    NavigationLink(destination: ScanView()) {
                        Text("Continue")
                    }
                }
                .padding()
                .accentColor(.white)
                .background(/*@START_MENU_TOKEN@*/Color.green/*@END_MENU_TOKEN@*/).cornerRadius(50)
            }
        }
    } 
}



struct LandingView_Previews: PreviewProvider {
    static var previews: some View {
        LandingView()
    }
}
