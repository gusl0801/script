# 검색할 도서 키워드
import sys
import DaumAPIServer
import OpenAPIServer

def PrintMenu():
    print("---------검색 기준--------------")
    print("(A/a) --- 소장 도서관")
    print("(S/s) --- 책 이름")
    print("(D/d) --- 책 등록 번호")
    print("(F/f) --- 저작자")
    print("(Z/z) --- 발행자")
    print("(X/x) --- ISBN")
    print("(C/c) --- 발행년도")
    print("(Q/q) --- 프로그램 종료")
    print("--------------------------------")

    return input()

def MenuHandler(sel):
    if sel is 'Q' or sel is 'q':
        sys.exit(1)
    if sel is 'A' or sel is 'a':
        return
    if sel is 'S' or sel is 's':
        return
    if sel is 'D' or sel is 'd':
        return
    if sel is 'F' or sel is 'f':
        return
    if sel is 'Z' or sel is 'z':
        return
    if sel is 'X' or sel is 'x':
        return
    if sel is 'C' or sel is 'c':
        return

def GetKeyword():
    return input("검색 키워드를 입력해주세요")
