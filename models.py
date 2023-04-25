from flask_sqlalchemy import SQLAlchemy
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime, Integer, func
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    firstName: Mapped[str]
    lastName: Mapped[str]
    emailId: Mapped[str]
    hometown: Mapped[str]
    roleId: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    role: Mapped["Role"] = relationship(backref="users")
    dateOfJoining: Mapped[datetime]
    # isApplicant: Mapped[bool]
    department: Mapped[str]
    ltcInfos: Mapped[List["LTCInfo"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __init__(self, json):
        self.firstName = json['firstName']
        self.lastName = json['lastName']
        self.emailId = json['emailId']
        self.hometown = json['hometown']
        self.dateOfJoining = datetime.strptime(json['dateOfJoining'], '%Y-%m-%d')
        self.department = json['department']
        # self.isApplicant = json['isApplicant']
        self.roleId = json['roleId']
        self.ltcInfos = []

    def __repr__(self):
        return "User{id: %s, name: %s, emailId: %s, dateOfJoining: %s}" % (
                self.id,
                self.firstName,
                self.emailId,
                self.dateOfJoining,
                )
    
    def json(self):
        return {
                "id": self.id,
                "firstName": self.firstName,
                "lastName": self.lastName,
                "emailId": self.emailId,
                "hometown": self.hometown,
                # "dateOfJoining": self.dateOfJoining,
                "dateOfJoining": self.dateOfJoining,
                "department": self.department,
                # "isApplicant": self.isApplicant,
                "roleId": self.roleId,
                "role": self.role.json()
                }


class PersonInvolvedLTC(db.Model):
    __tablename__ = "people_involved_ltc"
    id: Mapped[int] = mapped_column(primary_key=True)
    ltcId: Mapped[int] = mapped_column(ForeignKey(('ltc_infos.id')))
    # LTCId -> foreign key
    name: Mapped[str]
    back: Mapped[bool]
    age: Mapped[int]
    relation: Mapped[str]
    fromPlace: Mapped[str]
    toPlace: Mapped[str]
    modeOfTravel: Mapped[str]
    
    def json(self):
        return {
            "id": self.id,
            "ltcId": self.ltcId,
            "name": self.name,
            "back": self.back,
            "age": self.age,
            "relation": self.relation,
            "fromPlace": self.fromPlace,
            "toPlace": self.toPlace,
            "modeOfTravel": self.modeOfTravel,
            }


class Role(db.Model):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    designation: Mapped[str]
    payLevel: Mapped[int]
    stageCurrent: Mapped[str]
    nextStage: Mapped[str]
    prevStage: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return "Role {id: %s, designation: %s, payLevel: %s, stageCurrent: %s, nextStage: %s, prevStage: %s}" % (
                self.id,
                self.designation,
                self.payLevel,
                self.stageCurrent,
                self.nextStage,
                self.prevStage,
                )

    def json(self):
        return {
                "id": self.id,
                "designation": self.designation,
                "payLevel": self.payLevel,
                "stageCurrent": self.stageCurrent,
                "nextStage": self.nextStage,
                "prevStage": self.prevStage
            }




class LTCInfo(db.Model):
    __tablename__ = "ltc_infos"
    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates="ltcInfos")
    fromDate: Mapped[datetime]
    toDate: Mapped[datetime]
    prefixFrom: Mapped[datetime] = mapped_column(nullable=True)
    prefixTo: Mapped[datetime] = mapped_column(nullable=True)
    suffixFrom: Mapped[datetime] = mapped_column(nullable=True)
    suffixTo: Mapped[datetime] = mapped_column(nullable=True)
    # spouseEntitiled -> bool
    # spouseEntitledProof -> filepath
    earnedLeaveAvailed: Mapped[int]
    natureOfTravel: Mapped[str]
    placeToVisit: Mapped[str]
    totalEstimatedFare: Mapped[int]
    # peopleInvolvedinLTC  -> foreign key
    advanceRequired: Mapped[bool]
    encashmentAvailed: Mapped[bool]
    encashmentNoOfDays: Mapped[int]
    stageRedirect: Mapped[str] = mapped_column(nullable=True)
    stageCurrent: Mapped[str]
    fillDate: Mapped[datetime]
    hodDate: Mapped[datetime]= mapped_column(nullable=True)
    estabDate: Mapped[datetime]= mapped_column(nullable=True)
    accountsDate: Mapped[datetime]= mapped_column(nullable=True)
    auditDate: Mapped[datetime]= mapped_column(nullable=True)
    registrarDate: Mapped[datetime]= mapped_column(nullable=True)
    deanDate: Mapped[datetime]= mapped_column(nullable=True)
    peopleInvolved: Mapped[List["PersonInvolvedLTC"]] = relationship(backref='ltc_infos', cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(backref="ltc_infos")
    
    def __init__(self, json):
        peopleInvolvedinLTC = json.get('peopleInvolved', [])
        dateLog = json.get('dateLog', [])
        for person in peopleInvolvedinLTC:
            p = PersonInvolvedLTC(**person)
            self.peopleInvolved.append(PersonInvolvedLTC(**person))

        self.userId = json['userId']
        if json['fromDate'] != '':
            self.fromDate = datetime.strptime(json['fromDate'], '%Y-%m-%d')
        else:
            self.fromDate = None
        if json['toDate'] != '':
            self.toDate = datetime.strptime(json['toDate'], '%Y-%m-%d')
        else:
            self.toDate = None
        if json['prefixFrom'] != '':
            self.prefixFrom = datetime.strptime(json['prefixFrom'], '%Y-%m-%d')
        else:
            self.prefixFrom = None
        if json['prefixTo'] != '':
            self.prefixTo = datetime.strptime(json['prefixTo'], '%Y-%m-%d')
        else:
            self.prefixTo = None
        if json['suffixFrom'] != '':
            self.suffixFrom = datetime.strptime(json['suffixFrom'], '%Y-%m-%d')
        else:
            self.suffixFrom = None
        if json['suffixTo'] != '':
            self.suffixTo = datetime.strptime(json['suffixTo'], '%Y-%m-%d')
        else:
            self.suffixTo = None

        self.earnedLeaveAvailed = json['earnedLeaveAvailed']
        self.natureOfTravel = json['natureOfTravel']
        self.placeToVisit = json['placeToVisit']
        self.totalEstimatedFare = json['totalEstimatedFare']
        self.advanceRequired = json['advanceRequired']
        self.encashmentAvailed = json['encashmentAvailed']
        self.encashmentNoOfDays = json['encashmentNoOfDays']
        # self.stageRedirect = json.get('stageRedirect')
        # self.stageCurrent = json['stageCurrent']
        self.fillDate = datetime.now()
        self.stageRedirect = None
        self.stageCurrent = 1

    def __repr__(self):
        return "LTCInfo(id=%s, )" % (
                self.id
                )
    
    def json(self):
         return {
                "id": self.id,
                "user": self.user.json(),
                "userId": self.userId,
                "fromDate": self.fromDate,
                "toDate": self.toDate,
                "prefixFrom": self.prefixFrom,
                "prefixTo": self.prefixTo,
                "suffixFrom": self.suffixFrom,
                "suffixTo": self.suffixTo,
                "earnedLeaveAvailed": self.earnedLeaveAvailed,
                "natureOfTravel": self.natureOfTravel,
                "placeToVisit": self.placeToVisit,
                "totalEstimatedFare": self.totalEstimatedFare,
                "advanceRequired": self.advanceRequired,
                "encashmentAvailed": self.encashmentAvailed,
                "encashmentNoOfDays": self.encashmentNoOfDays,
                "stageRedirect": self.stageRedirect,
                "stageCurrent": self.stageCurrent,
                "fillDate": self.fillDate,
                "hodDate": self.hodDate,
                "estabDate": self.estabDate,
                "accountsDate": self.accountsDate,
                "auditDate": self.auditDate,
                "registrarDate": self.registrarDate,
                "deanDate": self.deanDate,
                "peopleInvolved": [person.json() for person in self.peopleInvolved]
                }

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    ltcId: Mapped[int] = mapped_column(ForeignKey(('ltc_infos.id')))
    comment: Mapped[str]
    stage: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    def __repr__(self):
        return f"Comment('{self.comment}' set by stage-{self.stage} user)"

    def json(self):
        return {
                "id": self.id,
                "ltcId": self.ltcId,
                "comment": self.comment,
                "stage": self.stage,
                "created_at": self.created_at,
                }
