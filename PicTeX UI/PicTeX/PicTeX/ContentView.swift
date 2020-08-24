//
//  ContentView.swift
//  PicTeX
//
//  Created by Erica Chiang on 8/23/20.
//  Copyright © 2020 Erica Chiang. All rights reserved.
//

import SwiftUI

struct ContentView : View {
    var body: some View {
        NavigationView {
            VStack {
                Text("Hello World")
                NavigationLink(destination: LandingView()) {
                    Text("Do Something")
                }
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
